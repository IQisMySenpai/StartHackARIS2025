import json
import os
from random import uniform

def config_load():
    # Load API Key from Config Json
    with open(os.path.join(os.path.dirname(__file__), "../config/config.json")) as f:
        data = json.load(f)
        return data

def generate_writing_duration():
    return uniform(1.5, 10) # uniform(1.5, 3)

