from typing import List
from pyargwriter.utils.type_testing import type_of_all

STR = "foo"
INT = 42
FLOAT = 3.141
BOOL_FALSE = False
BOOL_TRUE = True
EMPTY_LIST = []
INT_LIST = [1, 2, 3]
FLOAT_LIST = [4.5, 5.6, 6.7]
STR_LIST = ["a", "b", "cd", "efg"]
BOOL_LIST = [False, True, False, True]


class ArgumentTester:
    """This class contains public functions to in order to run the pyargwriter and test the created argument parser"""

    def __init__(self) -> None:
        """initialize class"""
        return

    def int_test(self, a: int, b: int = 0):
        """test integer arguments

        Args:
            a (int): value without default
            b (int, optional): value with default. Defaults to 0.
        """
        assert a == INT
        assert isinstance(a, int)
        assert b in [INT, 0]
        assert isinstance(b, int)

    def str_test(self, a: str, b: str = "bar"):
        """test string arguments

        Args:
            a (int): value without default
            b (int, optional): value with default. Defaults to 0.
        """
        assert a == STR
        assert isinstance(a, str)
        assert b in [STR, "bar"]
        assert isinstance(b, str)

    def float_test(self, a: float, b: float = 0.0):
        """test float arguments

        Args:
            a (int): value without default
            b (int, optional): value with default. Defaults to 0.
        """
        assert a == FLOAT
        assert isinstance(a, float)
        assert b in [FLOAT, 0.0]
        assert isinstance(b, float)

    def bool_false_test(self, a: bool, b: bool = False):
        """test float arguments

        Args:
            a (int): value without default
            b (int, optional): value with default. Defaults to 0.
        """
        assert a == BOOL_FALSE
        assert isinstance(a, bool)
        assert b in [BOOL_FALSE, BOOL_TRUE]
        assert isinstance(b, bool)

    def bool_true_test(self, a: bool, b: bool = True):
        """test bool arguments

        Args:
            a (int): value without default
            b (int, optional): value with default. Defaults to 0.
        """
        assert a == BOOL_TRUE
        assert isinstance(a, bool)
        assert b in [BOOL_FALSE, BOOL_TRUE]
        assert isinstance(b, bool)

    def list_int_test(self, a: list[int], b: list[int] = []):
        """test list of integer arguments

        Args:
            a (int): value without default
            b (int, optional): value with default. Defaults to 0.
        """
        assert type_of_all(a, int)
        assert isinstance(a, list)
        assert type_of_all(b, int)
        assert isinstance(b, list)

    def list_str_test(self, a: list[str], b: list[str] = []):
        """test list of str arguments

        Args:
            a (int): value without default
            b (int, optional): value with default. Defaults to 0.
        """
        assert type_of_all(a, str)
        assert isinstance(a, list)
        assert type_of_all(b, str)
        assert isinstance(b, list)

    def list_float_test(self, a: list[float], b: list[float] = []):
        """test list of float arguments

        Args:
            a (int): value without default
            b (int, optional): value with default. Defaults to 0.
        """
        assert type_of_all(a, float)
        assert isinstance(a, list)
        assert type_of_all(b, float)
        assert isinstance(b, list)

    def list_bool_test(self, a: list[bool], b: list[bool] = []):
        """test list of bool arguments

        Args:
            a (int): value without default
            b (int, optional): value with default. Defaults to 0.
        """
        assert type_of_all(a, bool)
        assert isinstance(a, list)
        assert type_of_all(b, bool)
        assert isinstance(b, list)

    def typing_list_int_test(self, a: List[int], b: List[int] = []):
        """test list of integer arguments

        Args:
            a (int): value without default
            b (int, optional): value with default. Defaults to 0.
        """
        assert type_of_all(a, int)
        assert isinstance(a, list)
        assert type_of_all(b, int)
        assert isinstance(b, list)

    def typing_list_str_test(self, a: List[str], b: List[str] = []):
        """test list of str arguments

        Args:
            a (int): value without default
            b (int, optional): value with default. Defaults to 0.
        """
        assert type_of_all(a, str)
        assert isinstance(a, list)
        assert type_of_all(b, str)
        assert isinstance(b, list)

    def typing_list_float_test(self, a: List[float], b: List[float] = []):
        """test list of float arguments

        Args:
            a (int): value without default
            b (int, optional): value with default. Defaults to 0.
        """
        assert type_of_all(a, float)
        assert isinstance(a, list)
        assert type_of_all(b, float)
        assert isinstance(b, list)

    def typing_list_bool_test(self, a: List[bool], b: List[bool] = []):
        """test list of bool arguments

        Args:
            a (int): value without default
            b (int, optional): value with default. Defaults to 0.
        """
        assert type_of_all(a, bool)
        assert isinstance(a, list)
        assert type_of_all(b, bool)
        assert isinstance(b, list)
