from test import (
    INT,
    STR,
    FLOAT,
    BOOL_FALSE,
    BOOL_TRUE,
)


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

    def list_int_test(self, a: bool, b: bool = True):
        """test list of integer arguments

        Args:
            a (int): value without default
            b (int, optional): value with default. Defaults to 0.
        """
        # TODO: not implemented
        return

    def list_str_test(self, a: list[str], b: list[str] = []):
        """test list of str arguments

        Args:
            a (int): value without default
            b (int, optional): value with default. Defaults to 0.
        """
        # TODO: not implemented
        return

    def list_float_test(self, a: list[float], b: list[float] = True):
        """test list of float arguments

        Args:
            a (int): value without default
            b (int, optional): value with default. Defaults to 0.
        """
        # TODO: not implemented
        return

    def list_bool_test(self, a: list[bool], b: list[bool] = True):
        """test list of bool arguments

        Args:
            a (int): value without default
            b (int, optional): value with default. Defaults to 0.
        """
        # TODO: not implemented
        return
