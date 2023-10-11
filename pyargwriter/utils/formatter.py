from abc import ABC, abstractmethod
import subprocess
from typing import List


class Formatter(ABC):
    """Abstract base class for code formatters.

    This class defines an abstract method 'format' that should be implemented by subclasses.
    Code formatters are used to automatically format source code files.

    Methods:
        format(self, files: List[str]) -> None:
            Abstract method to format the given list of source code files.

    """

    @abstractmethod
    def format(self):
        """Format the given list of source code files.

        Args:
            files (List[str]): A list of file paths to be formatted.

        Raises:
            NotImplementedError: This method should be implemented in subclasses.
        """
        raise NotImplementedError


class BlackFormatter(Formatter):
    """Formatter for code using the 'black' code formatter.

    This class implements the 'format' method to format source code files using the 'black' code formatter.

    Attributes:
        name (str): The name of the code formatter ('black').

    Methods:
        format(self, files: List[str]) -> None:
            Format the given list of source code files using 'black'.

    """

    def __init__(self) -> None:
        self.name = "black"

    def format(self, files: List[str]):
        files = " ".join(files)

        subprocess.run(f"black {files}", shell=True)
