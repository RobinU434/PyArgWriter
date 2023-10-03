

import json
import logging
import os
import yaml
from pathlib import Path


def write_yaml(data: dict, path: str):
    with open(path, 'w') as outfile:
        yaml.dump(data, outfile, default_flow_style=False)


def write_json(data: dict, path: str):
    with open(path, "w") as outfile:
        json.dump(data, outfile, indent=4)


def load_yaml(path) -> dict:
    with open(path, 'r') as file:
        data = yaml.safe_load(file)
    return data


def load_json(path) -> dict:
    with open(path, 'r') as file:
        data = json.load(file)
    return data


def create_directory(path: str):
    try:
        os.makedirs(path)
    except FileExistsError as e:
        logging.warning(str(e))

def create_file(file_path: str):
    f = open(file_path, "w")


def check_file_exists(file_path: str):
    file_path = Path(file_path)
    if file_path.exists():
        return True
    return False