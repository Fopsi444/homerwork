import logging
import requests


logger = logging.getLogger(__name__)

class SWAPIClient:
    def __init__(self, base_url: str):
        self.base_url = base_url

    def fetch_json(self, endpoint: str) -> list:
        all_data = []
        url = f"{self.base_url}{endpoint}"

        while url:
            try:
                logger.info(f"Fetching data from: {url}")
                response = requests.get(url)
                response.raise_for_status()
                data = response.json()
                all_data.extend(data['results'])
                url = data.get('next')
            except requests.exceptions.RequestException as e:
                logger.error(f"Request failed for {url}: {e}")
                break
        logger.info(f"Fetched {len(all_data)} records from {endpoint}")
        return all_data