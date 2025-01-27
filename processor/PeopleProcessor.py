
import pandas as pd
from EntityProcessor import EntityProcessor

class PeopleProcessor(EntityProcessor):
    def process(self, json_data: list) -> pd.DataFrame:

        df = pd.DataFrame(json_data)
        df['full_name'] = df['name']  
        return df
