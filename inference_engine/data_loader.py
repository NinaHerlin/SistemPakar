# inference_engine/data_loader.py
import json

def load_rules(path='rules.json'):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)
