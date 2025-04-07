import requests
from config import get_config

class ExampleAPIClient:
    def fetch_data(self):
        cfg = get_config()
        headers = {"Authorization": f"Bearer {cfg['api_key']}"} if cfg['api_key'] else {}
        response = requests.get(cfg["api_url"], headers=headers)
        response.raise_for_status()
        return response.json()
