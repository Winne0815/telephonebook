import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
config_file_name = "config.json"


class Config:

    @staticmethod
    def config():
        with open(BASE_DIR / config_file_name) as f:
            return json.load(f)
