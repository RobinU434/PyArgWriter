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
    """Load and parse a Python source file into an Abstract Syntax Tree (AST).

    This function reads a Python source file and parses it into an AST representation
    using Python's built-in ast module. The AST can then be traversed and analyzed
    to extract structural information about classes, functions, and their signatures.

    Args:
        file_path (str): Path to the Python source file to parse. The file should
            contain valid Python code.

    Returns:
        ast.Module: The root node of the parsed AST representing the entire module.

    Raises:
        FileNotFoundError: If the specified file_path does not exist.
        SyntaxError: If the Python source file contains syntax errors.

    Example:
        >>> tree = load_file_tree('my_module.py')
        >>> # Now you can traverse the tree using ast.NodeVisitor
    """
    with open(file_path, "r", encoding="utf-8") as file:
        tree = ast.parse(file.read())
    return tree


def get_project_root_name(path: str) -> str:
    """Extract the project root directory name from a given path.

    This function extracts the last directory name from a path string, which is typically
    the project root directory name. If the path is ".", it uses the current working directory.

    Args:
        path (str): A directory path (relative or absolute). Can be:
            - "." for current directory
            - "my_project" for a simple directory name
            - "/path/to/my_project" for an absolute path
            - "path/to/my_project/" for a relative path

    Returns:
        str: The name of the last directory in the path (project root name).

    Example:
        >>> get_project_root_name("/home/user/projects/my_app")
        'my_app'
        >>> get_project_root_name("my_app/")
        'my_app'
        >>> get_project_root_name(".")
        'current_directory_name'
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
