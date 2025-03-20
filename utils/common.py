import json
import os

def config_load():
    # Load API Key from Config Json
    with open(os.path.join(os.path.dirname(__file__), "../config/config.json")) as f:
        data = json.load(f)
        return data