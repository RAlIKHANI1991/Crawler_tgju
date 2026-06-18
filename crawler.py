import requests
import pandas as pd
import time
import random
import re
import os 
from tqdm import tqdm

def get_total(session, base_url, params_base):
    params = params_base.copy()
    params["draw"] = 1
    params["start"] = 0
    try:
        r = session.get(base_url, params=params, timeout=25)
        r.raise_for_status()
        #if r.status_code != 200:
         #  raise ValueError("خطا!")
        data = r.json()
        total = data.get("recordsTotal", 0)
        if total == 0:
            raise ValueError("NOT FIND NO RECORD - identifier IS IT WRONG?")
        return total, data.get("length", 30)  # length اگر dynamic بود
    except Exception as e:
        raise RuntimeError(f"EROR IN GETTING total: {e}")

def fetch_page(session, base_url, params_base, draw, start, length, retries=3):
    """گرفتن یک صفحه با retry"""
    params = params_base.copy()
    params["draw"] = draw
    params["start"] = start
    params["length"] = length
    params["_"] = int(time.time() * 1000)
    
    for attempt in range(1, retries + 1):
        try:
            r = session.get(base_url, params=params, timeout=25)
            r.raise_for_status()
            data = r.json()
            if str(data.get("draw")) != str(draw):
                raise ValueError("draw mismatch")
            return data.get("data", [])
        except Exception as e:
            print(f"TRY {attempt}/{retries} FAIL: {e}")
            time.sleep(random.uniform(2, 5) * attempt)  # exponential backoff
            
    raise RuntimeError("all try failed !! maybe you become lock")

# main function
def crawl_tgju(identifier, start_from=0, temp_csv=None, final_csv=None, min_sleep=3.0, max_sleep=10.0):

    DATA_DIR = "data"  # دایرکتوری ذخیره دیتا
    os.makedirs(DATA_DIR, exist_ok=True) # ساخت پوشه دیتا 

    if temp_csv is None:
        temp_csv = os.path.join(DATA_DIR, f"{identifier}_history_temp.csv")   
    if final_csv is None:
        final_csv = os.path.join(DATA_DIR, f"{identifier}_history_full.csv")
    
    base_url = f"https://api.tgju.org/v1/market/indicator/summary-table-data/{identifier}"

    session = requests.Session()
    session.headers.update({
           "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
           "Accept"    : "application/json, text/javascript, */*; q=0.01",
     "X-Requested-With": "XMLHttpRequest",
           "Referer"   : f"https://www.tgju.org/profile/{identifier}/history",   })
    
    params_base = {
        "lang": "fa",
        "order_dir": "asc",
        "order_dir": "",  # تکراری
        "columns[0][data]": "0", "columns[0][name]": "", "columns[0][searchable]": "true", "columns[0][orderable]": "true",
        "columns[0][search][value]": "", "columns[0][search][regex]": "false",
        # ... همه 8 بلوک رو اضافه کن
        "search": "",
        "order_col": "",
        "from": "",
        "to": "",
        "convert_to_ad": "1",
    }
    for i in range(1, 8):  # الگو برای بقیه
        params_base[f"columns[{i}][data]"] = str(i)
        params_base[f"columns[{i}][name]"] = ""
        params_base[f"columns[{i}][searchable]"] = "true"
        params_base[f"columns[{i}][orderable]"] = "true"
        params_base[f"columns[{i}][search][value]"] = ""
        params_base[f"columns[{i}][search][regex]"] = "false"
    
    total, length = get_total(session, base_url, params_base)
    print(f"Total Records: {total} | Length of Page: {length}")
    
    # late Load
    try:
        df_existing = pd.read_csv(temp_csv, encoding="utf-8-sig")
        all_rows = df_existing.values.tolist()
        print(f"Loaded: {len(all_rows)} Row")
    except FileNotFoundError:
        all_rows = []
    
    draw = (start_from // length) + 1
    start = max(start_from, len(all_rows))
    
    with tqdm(total=total, initial=start, desc="Get rows", unit="row") as pbar:
        while start < total:
            page_rows = fetch_page(session, base_url, params_base, draw, start, length)
            cleaned = clean_rows(page_rows)
            all_rows.extend(cleaned)
            pbar.update(len(cleaned))
            save_temp(all_rows, temp_csv)
            
            start += length
            draw += 1
            time.sleep(random.uniform(min_sleep, max_sleep))

    columns = ['بازگشایی', 'کمترین', 'بیشترین', 'پایانی', 'میزان تغییر', 'درصد تغییر', 'تاریخ میلادی', 'تاریخ شمسی']
    save_final(all_rows, final_csv, columns)
    
    return all_rows, total, length, draw, start


def save_temp(all_rows, temp_csv):
    #"""ذخیره موقت"""
    pd.DataFrame(all_rows).to_csv(temp_csv, index=False, encoding="utf-8-sig")
    print(f"ذخیره موقت: {temp_csv}")
    
def save_final(all_rows, final_csv, columns):
    """ذخیره نهایی : بدون کرش برای آیتم‌های مختلف"""
    if not all_rows:
        print("هیچ داده‌ای برای ذخیره وجود ندارد")
        return

    df = pd.DataFrame(all_rows, columns=columns)

    # تبدیل عددی ستون‌های قیمت و تغییر
    numeric_cols = ['بازگشایی', 'کمترین', 'بیشترین', 'پایانی', 'میزان تغییر']
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')

    # درصد تغییر – مقاوم در برابر string / float / NaN
    percent_col = 'درصد تغییر'
    if percent_col in df.columns:
        col_data = df[percent_col]

        if pd.api.types.is_numeric_dtype(col_data):
            # اگر از قبل عددی بود (مثل ons)
            df[percent_col] = col_data / 100
        else:
            # اگر string بود (مثل geram18)
            df[percent_col] = (
                col_data.astype(str)
                .str.replace(r'[%±]', '', regex=True)
                .str.strip()
                .replace(['', '-', '–', '−'], '0')
            )
            df[percent_col] = pd.to_numeric(df[percent_col], errors='coerce') / 100
    else:
        print(f"ستون '{percent_col}' وجود ندارد → رد شد")

    # حذف تکراری و مرتب‌سازی
    if 'تاریخ میلادی' in df.columns:
        df = df.drop_duplicates(subset=['تاریخ میلادی']).sort_values('تاریخ میلادی')
    else:
        df = df.drop_duplicates()

    df.to_csv(final_csv, index=False, encoding="utf-8-sig")
    print(f"فایل نهایی ذخیره شد: {final_csv} | ردیف‌ها: {len(df)}")

def clean_rows(page_rows):
    """تمیز کردن + تبدیل '-' و خالی به 0 در هر سلول که شبیه تغییر/درصد است"""
    cleaned = []
    for row in page_rows:
        new_row = []
        for cell in row:
            if isinstance(cell, str):
                cell = re.sub(r'<[^>]+>', '', cell)      # حذف HTML
                cell = cell.replace(',', '').strip()     # حذف کاما و فضای اضافی

                # اگر سلول شبیه مقدار تغییر یا درصد است (حاوی % یا فقط عدد با علامت)
                stripped = cell.strip()
                if stripped in ('', '-', '–', '−', '—', '+', '±') or not stripped:
                    cell = '0'
                elif '%' in stripped or '±' in stripped or stripped.lstrip('+-').replace('.', '', 1).isdigit():
                    cell = stripped.replace('%', '').replace('±', '').replace('–', '-').strip()
                    if not cell or cell in ('+', '-'):
                        cell = '0'

            new_row.append(cell)
        cleaned.append(new_row)
    return cleaned





