from __future__ import annotations

import logging
from typing import Any, Dict, List, Tuple, Type

from pyargwriter import TAB_SIZE
from pyargwriter.utils.decorator import overwrite_protection
from pyargwriter.utils.type_testing import type_of_all


class LineOfCode:
    """Represents a single line of code with indentation.

    This class represents a single line of code with a specified level of indentation.
    It is used to build code blocks and maintain proper indentation.

    Args:
        content (str): The content of the line of code.
        tab_level (int, optional): The level of indentation for the line. Defaults to 0.

    Attributes:
        tab_level (int): The level of indentation for the line.
        content (str): The content of the line of code.

    """

    def __init__(self, content: str, tab_level: int = 0) -> None:
        self._content: str = " " * (TAB_SIZE * tab_level) + content + "\n"
        self._tab_level = tab_level

    def __repr__(self) -> str:
        return self._content

    @property
    def tab_level(self) -> int:
        """The level of indentation for the line.

        Returns:
            int: The level of indentation for the line.
        """
        return self._tab_level

    @property
    def content(self) -> str:
        """The content of the line of code.

        Returns:
            str: The content of the line of code.
        """
        return self._content


class Code:
    """Represents a collection of code lines.

    This class represents a collection of code lines with indentation. It is used
    to build and manipulate code blocks.

    Attributes:
        _file (List[LineOfCode]): The list of code lines.
        _tab_level (int): The level of indentation for the code block.

    Methods:
        insert(self, content: List[LineOfCode] | LineOfCode | Code, index: int) -> None:
            Insert code lines at a specified index.

        append(self, content: str | Code | LineOfCode | List[LineOfCode]) -> None:
            Append code lines to the end of the code block.

        from_lines_of_code(cls: Code, code: List[LineOfCode]) -> Code:
            Create a Code instance from a list of LineOfCode objects.

        from_str(cls: Code, code: str) -> Code:
            Create a Code instance from a single string representing a line of code.

        _split_file(self, index: int) -> Tuple[List[LineOfCode], List[LineOfCode]]:
            Split the code block into two parts at the specified index.

        _insert_line_of_code(
            first: List[LineOfCode], line_of_code: LineOfCode, second: List[LineOfCode]
        ) -> List[LineOfCode]:
            Insert a single line of code into the code block.

        _insert_lines_of_code(
            first: List[LineOfCode],
            lines_of_code: List[LineOfCode],
            second: List[LineOfCode],
        ) -> List[LineOfCode]:
            Insert multiple lines of code into the code block.

        _insert_code(
            self, first: List[LineOfCode], code: Code, second: List[LineOfCode]
        ) -> List[LineOfCode]:
            Insert another Code instance into the code block.

        _write(self, path: str) -> None:
            Write the code block to a specified file path.

        file(self) -> List[LineOfCode]:
            Get the list of code lines in the code block.

        set_tab_level(self, tab_level: int) -> None:
            Set the tab level for all lines of code in the code block.

    """

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
        """Create a Code instance from a list of LineOfCode objects.

        Args:
            code (List[LineOfCode]): List of LineOfCode objects.

        Returns:
            Code: A Code instance containing the specified code lines.

        """
        obj = cls()
        obj.insert(code, 0)
        return obj

    @classmethod
    def from_str(cls: Code, code: str) -> Code:
        """Create a Code instance from a single string representing a line of code.

        Args:
            code (str): A single string representing a line of code.

        Returns:
            Code: A Code instance containing the specified code line.

        """
        line_of_code = LineOfCode(code)
        obj = cls.from_lines_of_code([line_of_code])
        return obj

    def insert(self, content: List[LineOfCode] | LineOfCode | Code, index: int) -> None:
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
            msg = f"Wrong type to insert into content. You provided: {type(content), isinstance(content, Code), type(self)}"
            logging.error(msg)
            return

        self._file = method(first, content, second)

    def _split_file(self, index: int) -> Tuple[List[LineOfCode], List[LineOfCode]]:
        """Split the code block into two parts at the specified index.

        Args:
            index (int): The index at which to split the code block.

        Returns:
            Tuple[List[LineOfCode], List[LineOfCode]]: A tuple containing two lists of code lines,
                the first part before the index and the second part after the index.

        """
        first = self._file[:index]
        second = self._file[index:]
        return first, second

    @staticmethod
    def _insert_line_of_code(
        first: List[LineOfCode], line_of_code: LineOfCode, second: List[LineOfCode]
    ) -> List[LineOfCode]:
        """Insert a single line of code into the code block.

        Args:
            first (List[LineOfCode]): The first part of the code block.
            line_of_code (LineOfCode): The line of code to insert.
            second (List[LineOfCode]): The second part of the code block.

        Returns:
            List[LineOfCode]: The updated code block with the line_of_code inserted.

        """
        return [*first, line_of_code, *second]

    @staticmethod
    def _insert_lines_of_code(
        first: List[LineOfCode],
        lines_of_code: List[LineOfCode],
        second: List[LineOfCode],
    ) -> List[LineOfCode]:
        """Insert multiple lines of code into the code block.

        Args:
            first (List[LineOfCode]): The first part of the code block.
            lines_of_code (List[LineOfCode]): The lines of code to insert.
            second (List[LineOfCode]): The second part of the code block.

        Returns:
            List[LineOfCode]: The updated code block with the lines_of_code inserted.

        """

        return [*first, *lines_of_code, *second]

    def _insert_code(
        self, first: List[LineOfCode], code: Code, second: List[LineOfCode]
    ) -> List[LineOfCode]:
        """Insert another Code instance into the code block.

        Args:
            first (List[LineOfCode]): The first part of the code block.
            code (Code): The Code instance to insert.
            second (List[LineOfCode]): The second part of the code block.

        Returns:
            List[LineOfCode]: The updated code block with the code inserted.

        """
        return self._insert_lines_of_code(first, code.file, second)

    def append(self, content: str | Code | LineOfCode | List[LineOfCode]) -> None:
        """Append content to the end of the code block.

        Args:
            content (str | Code | LineOfCode | List[LineOfCode]): Content to append.

        """
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
        """Write the code block to a file.

        Args:
            path (str): The file path where the code block should be written.

        """
        self._write(path=path)

    def write_force(self, path: str):
        """Write the code block to a file without asking if you to overwrite existing files.

        Args:
            path (str): The file path where the code block should be written.

        """
        self._write(path)

    def _write(self, path: str, encoding: str = "utf-8"):
        """Write the code block to a specified file path.

        Args:
            path (str): The file path where the code block should be written.
            encoding (str, optional): How to encode the text to write. Defaults to utf-8

        """
        msg = f"Create {path}"
        logging.info(msg)
        with open(path, "w", encoding=encoding) as text_file:
            text_file.write(repr(self))

    @property
    def file(self) -> List[LineOfCode]:
        """Get the list of code lines in the code block.

        Returns:
            List[LineOfCode]: The list of code lines.

        """
        return self._file

    def set_tab_level(self, tab_level: int) -> None:
        """Set the tab level for all lines of code in the code block.

        This method sets the tab level for all lines of code in the code block.
        It adjusts the indentation of each line based on the specified tab level.

        Args:
            tab_level (int): The tab level to set. Must be a non-negative integer.

        """
        if tab_level < 0:
            logging.warning("Given tab-level was smaller than 0. Set tab_level = 0")
            tab_level = 0

        first_tab_level = self._file[0].tab_level

        renewed_files: List[LineOfCode] = []
        for line in self._file:
            # reset by first tab-level
            content = line.content[(TAB_SIZE * first_tab_level) :]  # noqa: E203
            internal_tab_level = line.tab_level
            renewed_files.append(
                LineOfCode(content=content, tab_level=internal_tab_level + tab_level)
            )
        self._file = renewed_files


class Function(Code):
    """Represents a Python function.

    This class represents a Python function and allows you to build and manipulate its structure.

    Args:
        name (str): The name of the function.
        signature (Dict[str, Type], optional): A dictionary representing the function's signature.
        return_type (Type, optional): The return type of the function.

    Attributes:
        _name (str): The name of the function.
        _signature (Dict[str, Type]): A dictionary representing the function's signature.
        _return_type (Type): The return type of the function.

    Methods:
        __init__(self, name: str, signature: Dict[str, Type] = {}, return_type: Type = None) -> None:
            Initializes a new Function instance.

        _generate_header(self):
            Generates the function header based on the name, signature, and return type.

        name(self):
            Returns the name of the function.

        (other class methods...)

    """

    def __init__(
        self, name: str, signature: Dict[str, Type] = {}, return_type: Type = None
    ) -> None:
        super().__init__()

        self._name: str = name
        self._signature: Dict[str, str] = self._serialize_signature(signature)
        self._return_type_name: str = self._serialize_type(return_type)
        self._generate_header()

    def _serialize_signature(self, signature: Dict[str, Type]) -> Dict[str, str]:
        """serialized signature

        Args:
            signature (Dict[str, Type]): dict of variable names and type of variables

        Returns:
            Dict[str, str]: dictionary of variable names and name of types
        """
        result = {}
        for key, value in signature.items():
            result[key] = self._serialize_type(value)
        return result

    @staticmethod
    def _serialize_type(var_type: Type) -> str:
        if var_type is None:
            return "None"
        return var_type.__name__

    def _generate_header(self):
        """Generate the function header based on the name, signature, and return type."""
        signature = str(self._signature).strip("{}").replace("'", "")

        first_line = f"def {self._name}({signature})"

        if self._return_type_name:
            first_line += f" -> {str(self._return_type_name)}"
        first_line += ":"

        self.append(content=first_line)

        self._tab_level += 1

    @property
    def name(self):
        """Return the name of the function."""
        return self._name


class Match(Code):
    """Represents a Python 'match' expression.

    This class represents a 'match' expression in Python and allows you to build and manipulate its structure.

    Args:
        match_value (Any): The value to match against.
        body (Code): The code block representing the body of the 'match' expression.

    Attributes:
        _match_value (Any): The value to match against.
        body (Code): The code block representing the body of the 'match' expression.

    Methods:
        (other class methods...)

    """

    def __init__(self, match_value: Any, body: Code) -> None:
        super().__init__()
        self._match_value = match_value
        self.body = body
        self._generate()

    def _generate(self):
        """Generate the 'match' expression code based on the match value and body."""

        self.append(content=f"case {self.match_value}:")
        self._tab_level += 1
        self.append(self.body)

    @property
    def match_value(self) -> str:
        """Return a string representation of the match value."""
        match self._match_value:
            case str():
                return f"'{self._match_value}'"
            case float() | int():
                return str(self._match_value)
            case _:
                raise NotImplementedError(
                    f"Not implemented conversion type for {type(self._match_value)}"
                )


class DefaultCase(Match):
    def __init__(self, body: Code) -> None:
        super().__init__(None, body=body)

    def _generate(self):
        self.append(content="case _:")
        self._tab_level += 1
        self.append(self.body)


class MatchCase(Code):
    """Represents a 'case' in a Python 'match' expression.

    This class represents a 'case' in a Python 'match' expression and allows you to build and manipulate its structure.

    Args:
        match_name (str): The name of the matched value.
        matches (List[Match]): A list of Match objects representing different cases.

    Attributes:
        _name (str): The name of the matched value.
        _matches (List[Match]): A list of Match objects representing different cases.

    Methods:
        (other class methods...)

    """

    def __init__(self, match_name: str, matches: List[Match]) -> None:
        super().__init__()
        self._name = match_name
        self._matches = matches
        self._generate()

    def _generate(self):
        """Generate the 'case' block code for the 'match' expression."""
        self.append(content=f"match {self._name}:")
        self._tab_level += 1
        for match in self._matches:
            match.set_tab_level(1)
            self.append(match)
