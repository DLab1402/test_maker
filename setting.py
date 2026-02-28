import os
import sys
import json

def get_path(next_path=''):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(current_dir, next_path)

with open("config.json", "r") as file:
    data = json.load(file)

SOURCE_TYPE = data["source_type"]
DRIVE_LINK = data["drive_link"]
LOCAL_PATH = data["local_path"]
GUI_PATH = get_path("GUI/main.ui")