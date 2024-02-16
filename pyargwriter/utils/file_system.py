import ast
import json
import logging
import os
import yaml
from pathlib import Path


def write_yaml(data: dict, path: str) -> None:
    """Write data to a YAML file.

    Args:
        data (dict): The data to be written to the YAML file.
        path (str): The path to the YAML file.

    """
    with open(path, "w") as outfile:
        yaml.dump(data, outfile, default_flow_style=False)


def write_json(data: dict, path: str) -> None:
    """Write data to a JSON file.

    Args:
        data (dict): The data to be written to the JSON file.
        path (str): The path to the JSON file.

    """
    with open(path, "w") as outfile:
        json.dump(data, outfile, indent=4)


def load_yaml(path) -> dict:
    """Load data from a YAML file and return it as a dictionary.

    Args:
        path (str): The path to the YAML file.

    Returns:
        dict: The loaded data as a dictionary.

    """
    with open(path, "r") as file:
        data = yaml.safe_load(file)
    return data


def load_json(path) -> dict:
    """Load data from a JSON file and return it as a dictionary.

    Args:
        path (str): The path to the JSON file.

    Returns:
        dict: The loaded data as a dictionary.

    """
    with open(path, "r") as file:
        data = json.load(file)
    return data


def load_file_tree(file_path: str) -> ast.Module:
    """load programm ast tree at a given file

    Args:
        file_path (str): path to program file

    Returns:
        ast.Module: model tree
    """
    with open(file_path, "r", encoding="utf-8") as file:
        tree = ast.parse(file.read())
    return tree


def get_project_root_name(path: str) -> str:
    """looks for the project root directory

    Args:
        path (str): if there is a full relative or absolute path. Take the last directory name

    Returns:
        str: project root name
    """
    if path == ".":
        abs_path = os.getcwd()
        project_root_name = abs_path.split("/")[-1]
        return project_root_name
    else:
        path = path.rstrip("/")
        project_root_name = path.split("/")[-1]
        return project_root_name


def create_directory(path: str) -> None:
    """Create a directory if it doesn't already exist.

    Args:
        path (str): The path of the directory to create.

    """
    try:
        os.makedirs(path)
    except FileExistsError as e:
        logging.warning(str(e))


def create_file(file_path: str) -> None:
    """Create an empty file.

    Args:
        file_path (str): The path of the file to create.

    """

    f = open(file_path, "w", encoding="utf-8")
    f.close()


def check_file_exists(file_path: str) -> bool:
    """Check if a file exists at the specified path.

    Args:
        file_path (str): The path of the file to check.

    Returns:
        bool: True if the file exists, False otherwise.

    """
    file_path = Path(file_path)
    if file_path.exists():
        return True
    return False
