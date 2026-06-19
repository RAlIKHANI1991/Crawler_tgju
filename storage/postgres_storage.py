# storage/postgres_storage.py

from storage.base import BaseStorage


class PostgresStorage(BaseStorage):

    def load_temp(self):
        pass

    def save_temp(self, rows):
        pass

    def save_final(self, df):
        pass
    
'''    df.to_sql(
    "gold_history",
    self.engine,
    if_exists="append",
    index=False
)'''