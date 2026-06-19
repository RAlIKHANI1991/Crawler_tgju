# crawler/client.py

import random
import time
from tqdm import tqdm

from crawler.client import TGJUClient
from crawler.parser import build_params
from utils.cleaner import clean_rows
from utils.processor import build_dataframe


class TGJUCrawler:

    def __init__(self,identifier,storage,min_sleep=3,max_sleep=10):

        self.identifier = identifier
        self.storage = storage
        self.min_sleep = min_sleep
        self.max_sleep = max_sleep

        self.client = TGJUClient(identifier)

    def run(self):
        params = build_params()
        total, length = (self.client.get_total(params))

        rows = (self.storage.load_temp())
        start = len(rows)
        draw = (start // length) + 1

        with tqdm(total=total,initial=start,desc="crawl") as pbar:

            while start < total:
                page = (self.client.fetch_page(params,draw,start,length))

                cleaned = clean_rows(page)
                rows.extend(cleaned)
                self.storage.save_temp(rows)
                pbar.update(len(cleaned))
                start += length
                draw += 1
                time.sleep(random.uniform(self.min_sleep,self.max_sleep))

        df = build_dataframe(rows)

        self.storage.save_final(df)

        return df