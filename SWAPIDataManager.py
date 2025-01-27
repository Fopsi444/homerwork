
import logging
import pandas as pd
from processor.EntityProcessor import EntityProcessor

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

class SWAPIDataManager:
    def __init__(self, client):

        self.client = client
        self.df_list = {}
        self.processors = {}

    def register_processor(self, endpoint: str, processor: EntityProcessor):

        self.processors[endpoint] = processor

    def fetch_entity(self, endpoint: str):

        if endpoint in self.processors:
            raw_data = self.client.fetch_json(endpoint)
            processor = self.processors[endpoint]
            processed_data = processor.process(raw_data)
            self.df_list[endpoint] = processed_data
            logger.info(f"Отримано {len(raw_data)} записів для {endpoint}. Колонки: {processed_data.columns.tolist()}")
        else:
            logger.warning(f"Процесор для {endpoint} не знайдено")

    def apply_filter(self, endpoint: str, columns_to_drop: list):

        if endpoint in self.df_list:
            self.df_list[endpoint] = self.df_list[endpoint].drop(columns=columns_to_drop, errors='ignore')
            logger.info(f"Видалено колонки {columns_to_drop} для {endpoint}")
        else:
            logger.warning(f"Дані для {endpoint} не знайдено")

    def save_to_excel(self, file_name):

        logger.info(f"Запис даних у Excel файл: {file_name}")
        with pd.ExcelWriter(file_name) as writer:
            for endpoint, df in self.df_list.items():
                df.to_excel(writer, sheet_name=endpoint, index=False)
        logger.info("Дані успішно записано у Excel.")
