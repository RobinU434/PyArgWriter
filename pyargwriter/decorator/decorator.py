from typing import Callable
from functools import wraps
from hydra.main import _UNSPECIFIED_

from pyargwriter.utils.file_system import check_file_exists


def overwrite_protection(func: Callable) -> Callable:
    """Decorator to protect against overwriting existing files.

    This decorator is designed to be used with functions that write files. It will check if
    the file already exists and prompt the user for confirmation before overwriting it.

    Args:
        func (Callable): The function to be wrapped.

    Returns:
        Callable: The decorated function.

    Example:
        @overwrite_protection
        def save_data(data, path):
            # Your code to save data to a file here
            pass

    """

    def wrapper(*args, path: str, **kwargs):
        if check_file_exists(path):
            overwrite = input(f"{path} already exists. Overwrite it? [Y, n]: ")
            if overwrite.lower() not in ["", "y"]:
                return
        func(*args, path, **kwargs)

    return wrapper


def add_hydra(
    config_var_name: str = "cfg",
    version_base: str = _UNSPECIFIED_,
    config_path: str = _UNSPECIFIED_,
    config_name: str = None,
):
    def decorator(func: Callable):
        @wraps(func)
        def wrapper(*args, **kwargs):
            func(*args, **kwargs)
        return wrapper
    return decorator

