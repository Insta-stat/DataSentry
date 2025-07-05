import pandas as pd
from creds.accesses import api_key
from apify_client import ApifyClient
from config import INST_REAL_SCRAPER_ACTOR_ID, reels_input_data

client = ApifyClient(api_key)

run = client.actor(INST_REAL_SCRAPER_ACTOR_ID).call(run_input=reels_input_data)
dataset_items = client.dataset(run['defaultDatasetId']).list_items().items

df = pd.DataFrame(dataset_items)
df.to_csv('raw_data/reels.csv', index=False)
