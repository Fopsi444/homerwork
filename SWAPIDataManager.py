import logging
import pandas as pd

from FetchClass import SWAPIClient

logger = logging.getLogger(__name__)

class SWAPIDataManager:
    def __init__(self, client: 'SWAPIClient'):
        self.client = client
        self.df_list = {}

    def fetch_entity(self, endpoint: str):
        raw_data = self.client.fetch_json(endpoint)
        self.df_list[endpoint] = pd.DataFrame(raw_data)
        logger.info(f"Received {len(raw_data)} records for {endpoint}. Columns: {self.df_list[endpoint].columns.tolist()}")

    def apply_filter(self, endpoint: str, columns_to_drop: list):
        if endpoint in self.df_list:
            try:
                self.df_list[endpoint] = self.df_list[endpoint].drop(columns=columns_to_drop, errors='ignore')
                logger.info(f"Dropped columns {columns_to_drop} from {endpoint}")
            except Exception as e:
                logger.error(f"Error applying filter to {endpoint}: {e}")
        else:
            logger.warning(f"Data for {endpoint} not found, filter not applied.")

    def save_to_excel(self, file_name: str):
        logger.info(f"Saving data to Excel file: {file_name}")
        with pd.ExcelWriter(file_name) as writer:
            for endpoint, df in self.df_list.items():
                df.to_excel(writer, sheet_name=endpoint, index=False)
        logger.info(f"Data successfully saved to {file_name}")