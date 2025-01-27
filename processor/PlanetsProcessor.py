
import pandas as pd
from EntityProcessor import EntityProcessor

class PlanetsProcessor(EntityProcessor):
    def process(self, json_data: list) -> pd.DataFrame:

        df = pd.DataFrame(json_data)
        df['population'] = pd.to_numeric(df['population'], errors='coerce')
        return df
