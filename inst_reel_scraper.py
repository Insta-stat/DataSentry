import pandas as pd
import os
from apify_client import ApifyClient
from config import INST_REAL_SCRAPER_ACTOR_ID, reels_input_data

# Получаем API ключ из переменных окружения
api_key = os.getenv('APIFY_API')
if not api_key:
    raise ValueError("❌ API ключ Apify не найден. Убедитесь, что переменная окружения APIFY_API установлена.")

# Создаем директорию для данных, если её нет
os.makedirs('raw_data', exist_ok=True)

try:
    client = ApifyClient(api_key)
    
    # Запускаем сбор данных
    run = client.actor(INST_REAL_SCRAPER_ACTOR_ID).call(run_input=reels_input_data)
    dataset_items = client.dataset(run['defaultDatasetId']).list_items().items
    
    # Сохраняем результаты
    df = pd.DataFrame(dataset_items)
    df.to_csv('raw_data/reels.csv', index=False)
    
except Exception as e:
    raise Exception(f"❌ Ошибка при сборе данных: {str(e)}")
