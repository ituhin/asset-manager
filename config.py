import json

def load_config():
    """Load config from config.json"""
    with open("config/config.json", "r") as file:
        return json.load(file)