import pandas as pd

from storage.base import BaseStorage


class CSVStorage(BaseStorage):

    def __init__(self, temp_file, final_file):

        self.temp_file = temp_file
        self.final_file = final_file


    def load_temp(self):
        try:
            df = pd.read_csv(self.temp_file,encoding="utf-8-sig")
            return df.values.tolist()

        except FileNotFoundError:
            return []


    def save_temp(self, rows):
        pd.DataFrame(rows).to_csv(self.temp_file,index=False,encoding="utf-8-sig")


    def save_final(self, df):
        df.to_csv(self.final_file,index=False,encoding="utf-8-sig")