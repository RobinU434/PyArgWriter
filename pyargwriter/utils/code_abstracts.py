from __future__ import annotations

import logging
from decimal import Decimal
from typing import Any, Dict, List, Tuple, Type

from pyargwriter import TAB_SIZE
from pyargwriter.utils.decorator import overwrite_protection
from pyargwriter.utils.type_testing import type_of_all


class LineOfCode:
    def __init__(self, content: str, tab_level: int = 0) -> None:
        self._content: str = " " * (TAB_SIZE * tab_level) + content + "\n"
        self._tab_level = tab_level

    def __repr__(self) -> str:
        return self._content

    @property
    def tab_level(self) -> int:
        return self._tab_level

    @property
    def content(self) -> str:
        return self._content


class Code:
    def __init__(self) -> None:
        self._file: List[LineOfCode] = []
        self._tab_level: int = 0

    def __repr__(self) -> str:
        result = ""
        for line in self.file:
            result += repr(line)

        return result

    def __len__(self) -> int:
        return len(self._file)

    @classmethod
    def from_lines_of_code(cls: Code, code: List[LineOfCode]) -> Code:
        obj = cls()
        obj.insert(code, 0)
        return obj
    
    @classmethod
    def from_str(cls: Code, code: str) -> Code:
        line_of_code = LineOfCode(code)
        obj = cls.from_lines_of_code([line_of_code])
        return obj

    def insert(
        self, content: List[LineOfCode] | LineOfCode | Code, index: int
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
        self, first: List[LineOfCode], code: Code, second: List[LineOfCode]
    ) -> List[LineOfCode]:
        return self._insert_lines_of_code(first, code.file, second)

    def append(self, content: str | Code | LineOfCode | List[LineOfCode]) -> None:
        if isinstance(content, str):
            self._file.append(LineOfCode(content=content, tab_level=self._tab_level))
        elif isinstance(content, Code):
            content: Code
            content.set_tab_level(self._tab_level)
            self.insert(content, len(self))
        elif isinstance(content, LineOfCode) or (
            isinstance(content, list)
            and type_of_all(content, LineOfCode)
            and len(content)
        ):
            self.insert(content, len(self))

    @overwrite_protection
    def write(self, path: str) -> None:
        """where you want to save the file content.

        Args:
            path (str): path to file
        """
        self._write(path=path)

    def write_force(self, path: str):
        self._write(path)

    def _write(self, path: str):
        """where you want to save the file content.

        Args:
            path (str): path to file
        """
        logging.info(f"Create {path}")
        print("write")
        with open(path, "w") as text_file:
            text_file.write(repr(self))

    @property
    def file(self) -> List[LineOfCode]:
        return self._file

    def set_tab_level(self, tab_level: int) -> None:
        """sets tab level for all lines of code in self.file

        Args:
            tab_level (int): tab level. Has to be positive or zero
        """
        if tab_level < 0:
            logging.warning("Given tab-level was smaller than 0. Set tab_level = 0")
            tab_level = 0

        first_tab_level = self._file[0].tab_level

        renewed_files: List[LineOfCode] = []
        for line in self._file:
            # reset by first tab-level
            content = line.content[TAB_SIZE * first_tab_level :]
            internal_tab_level = line.tab_level
            renewed_files.append(
                LineOfCode(content=content, tab_level=internal_tab_level + tab_level)
            )
        self._file = renewed_files


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

        self.append(content=first_line)

        self._tab_level += 1

    @property
    def name(self):
        return self._name


class Match(Code):
    def __init__(self, match_value: Any, body: Code) -> None:
        super().__init__()
        self._match_value = match_value
        self.body = body
        self._generate()

    def _generate(self):
        self.append(content=f"case {self.match_value}:")
        self._tab_level += 1
        self.append(self.body)
        
    @property
    def match_value(self) -> str:
        match self._match_value:
            case str():
                return f"'{self._match_value}'"
            case float() | int():
                return str(self._match_value)
            case _:
                raise NotImplementedError(
                    f"Not implemented conversion type for {type(self._match_value)}"
                )


class MatchCase(Code):
    def __init__(self, match_name: str, matches: List[Match]) -> None:
        super().__init__()
        self._name = match_name
        self._matches = matches
        print(matches)
        self._generate()

    def _generate(self):
        self.append(content=f"match {self._name}:")
        self._tab_level += 1
        for match in self._matches:
            match.set_tab_level(1)
            self.append(match)
