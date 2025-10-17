"""Test cases for pyargwriter._core.code_abstracts module.

This module contains comprehensive tests for the code abstraction classes:
LineOfCode, Code, Function, Match, MatchCase, and DefaultCase.
"""

import pytest
from pyargwriter._core.code_abstracts import (
    LineOfCode,
    Code,
    Function,
    Match,
    MatchCase,
    DefaultCase,
)
from pyargwriter import TAB_SIZE


class TestLineOfCode:
    """Test cases for LineOfCode class."""

    def test_line_of_code_creation_no_indentation(self):
        """Test creating a line of code without indentation."""
        line = LineOfCode("print('Hello')")
        assert line.content == "print('Hello')\n"
        assert line.tab_level == 0

    def test_line_of_code_creation_with_indentation(self):
        """Test creating a line of code with indentation."""
        line = LineOfCode("print('Hello')", tab_level=2)
        expected_indent = " " * (TAB_SIZE * 2)
        assert line.content == f"{expected_indent}print('Hello')\n"
        assert line.tab_level == 2

    def test_line_of_code_repr(self):
        """Test string representation of LineOfCode."""
        line = LineOfCode("x = 10", tab_level=1)
        expected_indent = " " * TAB_SIZE
        assert repr(line) == f"{expected_indent}x = 10\n"

    def test_line_of_code_property_accessors(self):
        """Test property accessors for LineOfCode."""
        line = LineOfCode("result = a + b", tab_level=3)
        assert line.tab_level == 3
        expected_indent = " " * (TAB_SIZE * 3)
        assert line.content == f"{expected_indent}result = a + b\n"


class TestCode:
    """Test cases for Code class."""

    def test_code_creation_empty(self):
        """Test creating an empty Code block."""
        code = Code()
        assert len(code) == 0
        assert repr(code) == ""

    def test_code_append_string(self):
        """Test appending a string to Code."""
        code = Code()
        code.append("line1")
        code.append("line2")
        assert len(code) == 2
        assert "line1\n" in repr(code)
        assert "line2\n" in repr(code)

    def test_code_append_line_of_code(self):
        """Test appending a LineOfCode object."""
        code = Code()
        line = LineOfCode("test line", tab_level=1)
        code.append(line)
        assert len(code) == 1
        assert "test line\n" in repr(code)

    def test_code_from_str(self):
        """Test creating Code from a string."""
        code = Code.from_str("single_line")
        assert len(code) == 1
        assert "single_line\n" in repr(code)

    def test_code_from_lines_of_code(self):
        """Test creating Code from list of LineOfCode objects."""
        lines = [
            LineOfCode("line1"),
            LineOfCode("line2"),
            LineOfCode("line3"),
        ]
        code = Code.from_lines_of_code(lines)
        assert len(code) == 3

    def test_code_insert_line_at_index(self):
        """Test inserting a line at specific index."""
        code = Code()
        code.append("line1")
        code.append("line3")
        code.insert(LineOfCode("line2"), 1)
        assert len(code) == 3
        lines = repr(code).split("\n")
        assert "line1" in lines[0]
        assert "line2" in lines[1]
        assert "line3" in lines[2]

    def test_code_insert_multiple_lines(self):
        """Test inserting multiple lines at once."""
        code = Code()
        code.append("line1")
        code.append("line4")
        lines_to_insert = [LineOfCode("line2"), LineOfCode("line3")]
        code.insert(lines_to_insert, 1)
        assert len(code) == 4

    def test_code_insert_code_block(self):
        """Test inserting another Code block."""
        code1 = Code()
        code1.append("main1")
        code1.append("main2")

        code2 = Code()
        code2.append("insert1")
        code2.append("insert2")

        code1.insert(code2, 1)
        assert len(code1) == 4

    def test_code_replace_line(self):
        """Test replacing a line at specific index."""
        code = Code()
        code.append("old_line")
        code.replace(LineOfCode("new_line"), 0)
        assert "new_line\n" in repr(code)
        assert "old_line" not in repr(code)

    def test_code_contains_string(self):
        """Test checking if Code contains a string."""
        code = Code()
        code.append("test_content")
        assert "test_content" in code
        assert "nonexistent" not in code

    def test_code_contains_line_of_code(self):
        """Test checking if Code contains a LineOfCode."""
        code = Code()
        line = LineOfCode("specific_line")
        code.append(line)
        assert line in code

    def test_code_set_tab_level(self):
        """Test setting tab level for all lines."""
        code = Code()
        code.append("line1")
        code.append("line2")
        code.set_tab_level(2)
        
        expected_indent = " " * (TAB_SIZE * 2)
        result = repr(code)
        assert result.startswith(expected_indent)

    def test_code_set_tab_level_negative(self):
        """Test that negative tab level is clamped to 0."""
        code = Code()
        code.append("line")
        code.set_tab_level(-1)
        assert not repr(code).startswith(" ")

    def test_code_get_line(self):
        """Test getting a specific line by index."""
        code = Code()
        line1 = LineOfCode("first")
        line2 = LineOfCode("second")
        code.append(line1)
        code.append(line2)
        
        retrieved = code.get_line(0)
        assert retrieved.content == line1.content


class TestFunction:
    """Test cases for Function class."""

    def test_function_simple_creation(self):
        """Test creating a simple function without arguments."""
        func = Function("my_func")
        result = repr(func)
        # Function without explicit return type gets "-> None"
        assert "def my_func()" in result

    def test_function_with_signature(self):
        """Test creating a function with argument signature."""
        func = Function("add_numbers", signature={"a": int, "b": int})
        result = repr(func)
        # Function without explicit return type gets "-> None"
        assert "def add_numbers(a: int, b: int)" in result

    def test_function_with_return_type(self):
        """Test creating a function with return type."""
        func = Function("get_value", return_type=str)
        result = repr(func)
        assert "def get_value() -> str:" in result

    def test_function_with_signature_and_return(self):
        """Test creating a function with both signature and return type."""
        func = Function("multiply", signature={"x": float, "y": float}, return_type=float)
        result = repr(func)
        assert "def multiply(x: float, y: float) -> float:" in result

    def test_function_append_body(self):
        """Test appending body content to function."""
        func = Function("test_func")
        func.append("result = 42")
        func.append("return result")
        result = repr(func)
        assert "result = 42" in result
        assert "return result" in result

    def test_function_name_property(self):
        """Test accessing function name property."""
        func = Function("my_special_func")
        assert func.name == "my_special_func"

    def test_function_with_dict_type(self):
        """Test function with Dict type annotation."""
        from typing import Dict
        func = Function("process", signature={"data": Dict[str, int]}, return_type=Dict[str, str])
        result = repr(func)
        assert "Dict[str, int]" in result
        assert "Dict[str, str]" in result

    def test_function_with_tuple_type(self):
        """Test function with Tuple type annotation."""
        from typing import Tuple
        func = Function("get_coords", return_type=Tuple[int, int])
        result = repr(func)
        assert "Tuple[int, int]" in result


class TestMatch:
    """Test cases for Match class."""

    def test_match_with_string_value(self):
        """Test creating a match case with string value."""
        body = Code.from_str("print('matched')")
        match = Match("option1", body)
        result = repr(match)
        assert "case 'option1':" in result
        assert "print('matched')" in result

    def test_match_with_int_value(self):
        """Test creating a match case with integer value."""
        body = Code.from_str("print('number')")
        match = Match(42, body)
        result = repr(match)
        assert "case 42:" in result

    def test_match_with_float_value(self):
        """Test creating a match case with float value."""
        body = Code.from_str("print('decimal')")
        match = Match(3.14, body)
        result = repr(match)
        assert "case 3.14:" in result

    def test_match_with_complex_body(self):
        """Test match with multi-line body."""
        body = Code()
        body.append("x = 10")
        body.append("y = 20")
        body.append("return x + y")
        match = Match("calculate", body)
        result = repr(match)
        assert "x = 10" in result
        assert "y = 20" in result
        assert "return x + y" in result

    def test_match_unsupported_type(self):
        """Test that unsupported match value types raise NotImplementedError."""
        body = Code.from_str("pass")
        # The error is raised during initialization when calling _generate()
        with pytest.raises(NotImplementedError):
            match = Match([1, 2, 3], body)


class TestDefaultCase:
    """Test cases for DefaultCase class."""

    def test_default_case_creation(self):
        """Test creating a default case."""
        body = Code.from_str("return False")
        default = DefaultCase(body)
        result = repr(default)
        assert "case _:" in result
        assert "return False" in result

    def test_default_case_with_complex_body(self):
        """Test default case with multi-line body."""
        body = Code()
        body.append("print('default')")
        body.append("return None")
        default = DefaultCase(body)
        result = repr(default)
        assert "case _:" in result
        assert "print('default')" in result
        assert "return None" in result


class TestMatchCase:
    """Test cases for MatchCase class."""

    def test_match_case_simple(self):
        """Test creating a simple match statement."""
        case1 = Match("a", Code.from_str("print('A')"))
        case2 = Match("b", Code.from_str("print('B')"))
        default = DefaultCase(Code.from_str("print('other')"))
        
        match_case = MatchCase("value", [case1, case2, default])
        result = repr(match_case)
        
        assert "match value:" in result
        assert "case 'a':" in result
        assert "print('A')" in result
        assert "case 'b':" in result
        assert "print('B')" in result
        assert "case _:" in result
        assert "print('other')" in result

    def test_match_case_with_integers(self):
        """Test match statement with integer cases."""
        case1 = Match(1, Code.from_str("return 'one'"))
        case2 = Match(2, Code.from_str("return 'two'"))
        default = DefaultCase(Code.from_str("return 'other'"))
        
        match_case = MatchCase("number", [case1, case2, default])
        result = repr(match_case)
        
        assert "match number:" in result
        assert "case 1:" in result
        assert "case 2:" in result

    def test_match_case_complex_bodies(self):
        """Test match with complex multi-line case bodies."""
        body1 = Code()
        body1.append("x = 10")
        body1.append("return x * 2")
        
        body2 = Code()
        body2.append("y = 20")
        body2.append("return y / 2")
        
        case1 = Match("double", body1)
        case2 = Match("half", body2)
        default = DefaultCase(Code.from_str("return 0"))
        
        match_case = MatchCase("operation", [case1, case2, default])
        result = repr(match_case)
        
        assert "match operation:" in result
        assert "x = 10" in result
        assert "y = 20" in result

    def test_match_case_empty_matches(self):
        """Test creating match case with only default."""
        default = DefaultCase(Code.from_str("pass"))
        match_case = MatchCase("value", [default])
        result = repr(match_case)
        assert "match value:" in result
        assert "case _:" in result


class TestCodeIntegration:
    """Integration tests for Code classes working together."""

    def test_nested_code_blocks(self):
        """Test nesting code blocks within each other."""
        outer = Code()
        outer.append("# Outer block")
        
        inner = Code()
        inner.append("# Inner block")
        inner.append("x = 10")
        
        outer.append(inner)
        outer.append("# Back to outer")
        
        result = repr(outer)
        assert "# Outer block" in result
        assert "# Inner block" in result
        assert "x = 10" in result
        assert "# Back to outer" in result

    def test_function_with_match_case(self):
        """Test creating a function containing a match statement."""
        func = Function("process_command", signature={"cmd": str}, return_type=bool)
        
        case1 = Match("start", Code.from_str("return True"))
        case2 = Match("stop", Code.from_str("return True"))
        default = DefaultCase(Code.from_str("return False"))
        
        match_case = MatchCase("cmd", [case1, case2, default])
        func.append(match_case)
        
        result = repr(func)
        assert "def process_command(cmd: str) -> bool:" in result
        assert "match cmd:" in result
        assert "case 'start':" in result
        assert "case 'stop':" in result
        assert "case _:" in result

    def test_code_write_to_file(self, tmp_path):
        """Test writing Code to a file."""
        code = Code()
        code.append("# Test file")
        code.append("def hello():")
        code._tab_level = 1
        code.append("print('Hello, world!')")
        
        file_path = tmp_path / "test_output.py"
        code.write_force(str(file_path))
        
        assert file_path.exists()
        content = file_path.read_text()
        assert "# Test file" in content
        assert "def hello():" in content
        assert "print('Hello, world!')" in content
