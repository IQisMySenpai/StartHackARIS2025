import json
import os
from random import uniform

def config_load():
    # Load API Key from Config Json
    with open(os.path.join(os.path.dirname(__file__), "../config/config.json")) as f:
        data = json.load(f)
        return data

def generate_writing_duration(msg):
    msg_length = len(msg)
    avg_chars_per_s = 10 + uniform(-0.1, 0.1)

    duration = (msg_length / avg_chars_per_s) + uniform(-2, 2)
    print(f'Waiting for {duration} seconds')
    return duration

