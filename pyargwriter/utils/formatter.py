

from abc import ABC, abstractmethod
import subprocess
from typing import List


class Formatter(ABC):
    @abstractmethod
    def format(self):
        raise NotImplementedError

class BlackFormatter(Formatter):
    def __init__(self) -> None:
        self.name = "black"

    def format(self, files: List[str]):
        files = " ".join(files)
        
        subprocess.run(f"black {files}", shell=True)