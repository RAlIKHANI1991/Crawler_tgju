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

'''
dict_tgju_total = {
    'tala18ayar' : 'geram18' , 
    'tala24ayar' : 'geram24' , 
    'tala740ayar': 'gold_740k' , 
    'tala2hand'  : 'gold_mini_size' , 

    'seke_Emami_naghdi'   : 'sekee' , 
    'seke_bahar_naghdi'   : 'sekeb' , 
    'nim_seke_naghdi'     : 'nim' , 
    'rob_seke_naghdi'     : 'rob' , 
    'seke_gerami_naghdi'  : 'gerami' , 

    'seke_Emami_takforoshi'   : 'retail_sekee' , 
    'seke_bahar_takforoshi'   : 'retail_sekeb' , 
    'nim_seke_takforoshi'     : 'retail_nim' , 
    'rob_seke_takforoshi'     : 'retail_rob' , 
    'seke_gerami_takforoshi'  : 'retail_gerami' , 

    'abshode_naghdi'    : 'gold_futures' , 
    'abshode_bonakdari' : 'gold_melted_wholesale' , 
         'Mazane'       : 'mesghal' , 

    'onse_gold'   : 'ons' , 
    'onse_silver' : 'silver' , 

    'dollar_azad' : 'price_dollar_rl' , 
      'euro'      : 'price_eur' , 
      'derham'    : 'price_aed'

}
'''