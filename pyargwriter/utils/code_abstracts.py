import logging
from typing import Dict, Tuple, Type, List
from pyargwriter.utils.decorator import overwrite_protection

from pyargwriter.utils.type_testing import type_of_all


class LineOfCode:
    def __init__(self, content: str, tab_level: int = 0) -> None:
        self._content: str = " " * (4 * tab_level) + content + "\n"

    def __repr__(self) -> str:
        return self._content


class Code:
    def __init__(self) -> None:
        self._file: List[LineOfCode] = []
        self._tab_level: int = 0

    def __repr__(self) -> str:
        result = ""
        for line in self._file:
            result += repr(line)

        return result

    def insert(
        self, content: List[LineOfCode] | LineOfCode | "Code", index: int
    ) -> None:
        """insert given lines of code into self._file of class at given index

        Args:
            content (List[LineOfCode] | LineOfCode): Lines of code to insert
            index (int): Where to insert the given content
        """
        first, second = self._split_file(index)

        # insert content
        if (
            isinstance(content, list)
            and type_of_all(content, LineOfCode)
            and len(content)
        ):
            method = self._insert_lines_of_code
        elif isinstance(content, LineOfCode):
            method = self._insert_line_of_code
        elif isinstance(content, Code):
            method = self._insert_code
        else:
            logging.error(
                f"Wrong type to insert into content. You provided: {type(content), type(content) == Code, type(self)}"
            )
            return

        self._file = method(first, content, second)

    def _split_file(self, index: int) -> Tuple[List[LineOfCode], List[LineOfCode]]:
        first = self._file[:index]
        second = self._file[index:]
        return first, second

    @staticmethod
    def _insert_line_of_code(
        first: List[LineOfCode], line_of_code: LineOfCode, second: List[LineOfCode]
    ) -> List[LineOfCode]:
        return [*first, line_of_code, *second]

    @staticmethod
    def _insert_lines_of_code(
        first: List[LineOfCode],
        lines_of_code: List[LineOfCode],
        second: List[LineOfCode],
    ) -> List[LineOfCode]:
        return [*first, *lines_of_code, *second]

    def _insert_code(
        self, first: List[LineOfCode], code: "Code", second: List[LineOfCode]
    ) -> List[LineOfCode]:
        return self._insert_lines_of_code(first, code.file, second)

    def append_line(self, content: str):
        self._file.append(LineOfCode(content=content, tab_level=self._tab_level))
    
    @overwrite_protection
    def write(self, path: str) -> None:
        """where you want to save the file content.

        Args:
            path (str): path to file
        """
        with open(path, "w") as text_file:
            text_file.write(repr(self))

    @property
    def file(self) -> List[LineOfCode]:
        return self._file


class Function(Code):
    def __init__(
        self, name: str, signature: Dict[str, Type] = {}, return_type: Type = None
    ) -> None:
        super().__init__()

        self._name = name
        self._signature = signature
        self._return_type = return_type
        self._generate_header()

    def _generate_header(self):
        signature = str(self._signature).strip("{}").replace("'", "")

        first_line = f"def {self._name}({signature})"

        if self._return_type:
            first_line += f" -> {str(self._return_type)}"
        first_line += ":"

        self.append_line(content=first_line)

        self._tab_level += 1

    @property
    def name(self):
        return self._name
