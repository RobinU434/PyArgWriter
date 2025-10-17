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
    """Decorator to mark a method for Hydra configuration integration.

    This decorator is used to indicate that a method should receive Hydra configuration
    management. When PyArgWriter processes this decorated method, it will generate
    appropriate ArgumentParser code that integrates with Hydra for configuration management.

    Args:
        config_var_name (str, optional): The name of the parameter that will receive the
            Hydra configuration object. Defaults to "cfg".
        version_base (str, optional): Hydra version base parameter. Defaults to _UNSPECIFIED_.
        config_path (str, optional): Relative path to the configuration directory.
            Defaults to _UNSPECIFIED_.
        config_name (str, optional): Name of the configuration file to load.
            Defaults to None.

    Returns:
        Callable: The decorator function that wraps the target method.

    Example:
        >>> @add_hydra(config_var_name="config", config_path="conf", config_name="app")
        >>> def train_model(self, config):
        >>>     print(f"Learning rate: {config.lr}")
        >>>     # Training logic here

    Note:
        This decorator is primarily used as a marker for PyArgWriter's code generation.
        The actual Hydra integration is handled by the generated ArgumentParser code.
    """
    def decorator(func: Callable):
        @wraps(func)
        def wrapper(*args, **kwargs):
            func(*args, **kwargs)
        return wrapper
    return decorator

