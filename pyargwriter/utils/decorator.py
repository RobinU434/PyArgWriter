import os
from typing import Callable

from pyargwriter.utils.file_system import check_file_exists


def cleanup_tests(func: Callable) -> Callable:
    def wrapper(*args, **kwargs):
        func(*args, **kwargs)

        os.system("rm ./tests/temp/*.py")
        os.system("rm ./tests/temp/*/*.py")

    return wrapper


def overwrite_protection(func: Callable) -> Callable:
    def wrapper(*args, path: str, **kwargs):
        if check_file_exists(path):
            overwrite = input(f"{path} already exists. Overwrite it? [Y, n]: ")
            if overwrite.lower() in ["", "y"]:
                func(*args, path, **kwargs)
    
    return wrapper