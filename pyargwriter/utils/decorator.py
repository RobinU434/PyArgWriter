import os
from typing import Callable


def cleanup_tests(func: Callable) -> Callable:
    def wrapper(*args, **kwargs):
        func(*args, **kwargs)

        os.system("rm ./tests/temp/*.py")
        os.system("rm ./tests/temp/*/*.py")

    return wrapper
