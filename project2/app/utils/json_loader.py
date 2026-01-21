import json


def load_json():
    with open("data.json", "r") as f:
        return json.load(f)
