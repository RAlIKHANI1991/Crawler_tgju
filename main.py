from storage.csv_storage import CSVStorage
from crawler.crawler import TGJUCrawler

identifier = "geram18"

storage = CSVStorage(temp_file  = f"data/{identifier}_temp.csv",
                     final_file = f"data/{identifier}_final.csv")
#storage = PostgresStorage(...)

crawler = TGJUCrawler(
    identifier=identifier,
    storage=storage,
    min_sleep=3,
    max_sleep=10
)

df = crawler.run()

print(df.head())

