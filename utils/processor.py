# utils/processor.py

import pandas as pd

COLUMNS = [
    'بازگشایی',
    'کمترین',
    'بیشترین',
    'پایانی',
    'میزان تغییر',
    'درصد تغییر',
    'تاریخ میلادی',
    'تاریخ شمسی'
]


def build_dataframe(rows):

    df = pd.DataFrame(rows,columns=COLUMNS)

    numeric_cols = [
        'بازگشایی',
        'کمترین',
        'بیشترین',
        'پایانی',
        'میزان تغییر'
    ]

    for col in numeric_cols:

        df[col] = pd.to_numeric(df[col],errors="coerce")

    percent_col = "درصد تغییر"

    if percent_col in df.columns:

        if pd.api.types.is_numeric_dtype(df[percent_col]):
            df[percent_col] = (df[percent_col] / 100)

        else:
            df[percent_col] = (
                df[percent_col].astype(str)
                .str.replace(r'[%±]','',regex=True)
                .str.strip()
                .replace(['', '-', '–', '−'],'0')
            )

            df[percent_col] = (pd.to_numeric(df[percent_col],errors='coerce') / 100)

    if "تاریخ میلادی" in df.columns:
        df = (df.drop_duplicates(subset=["تاریخ میلادی"]).sort_values("تاریخ میلادی"))

    return df