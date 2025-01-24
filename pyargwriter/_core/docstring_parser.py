from abc import ABC, abstractmethod
from ast import ClassDef, FunctionDef
import ast
import logging
import re
from typing import Dict


class DocstringParser(ABC):
    default_help_msg = "--no-documentation-exists--"

    def __init__(self):
        super().__init__()

    def _check_for_docstring(self, node: FunctionDef):
        doc_str = ast.get_docstring(node)
        if doc_str is None:
            msg = f"No docstring for method {node.name} available"
            logging.fatal(msg)
            error_msg = f"Process was aborted because of missing doc-string in function: {node.name}"
            raise ValueError(error_msg)

    @abstractmethod
    def get_help_msg(self, node: FunctionDef | ClassDef) -> str:
        """get first line of docstring

        Args:
            node (FunctionDef | ClassDef): ast object to extract docstring from

        Returns:
            str: first line of docstring
        """
        raise NotImplementedError

    @abstractmethod
    def get_arg_help_msg(self, node: FunctionDef) -> Dict[str, str]:
        """get key value pairs of arg_name and its help message

        Args:
            node (FunctionDef): where to extract the docstring from

        Returns:
            Dict[str, str]: arg_name: help message
        """
        raise NotImplementedError

    @abstractmethod
    def get_return_msg(self, node: FunctionDef) -> str:
        """get help message of return type

        Args:
            node (FunctionDef): where to extract docstring from

        Returns:
            str: help message of return type
        """
        raise NotImplementedError

    @classmethod
    def build_parser(cls, docstring_format: str) -> "DocstringParser":
        class_dict = {
            "epytext": EpyTextParser,
            "rest": ReSTParser,
            "google": GoogleParser,
            "numpydoc": NumpyDocParser,
        }
        return class_dict[docstring_format.lower()]()


class GoogleParser(DocstringParser):
    def __init__(self):
        super().__init__()

    def get_help_msg(self, node):
        docstring = ast.get_docstring(node)
        if docstring is None:
            logging.info(f"No docstring in {node.name} found.")
            msg = self.default_help_msg
        else:
            msg = docstring.split("\n")[0]

        return msg

    def get_arg_help_msg(self, node):
        docstring = ast.get_docstring(node)
        num_args = len(node.args.args)
        if num_args == 0:
            return dict()
        elif num_args == 1 and node.args.args[0].arg == "self":
            return dict()

        # if there is no documentation
        if docstring is None:
            keys = [arg.arg for arg in node.args.args]
            if "self" in keys:
                keys.remove("self")
            values = [self.default_help_msg] * len(keys)
            res = dict(zip(keys, values))
            return res

        # if there is a sufficient docstring -> extract message
        docstring: list[str] = docstring.split("\n")
        args_start = docstring.index("Args:")
        res = {}
        for idx in range(args_start + 1, args_start + num_args):
            splits = docstring[idx].strip(" ").split(":")
            arg = splits[0]
            # delete bracket with type information
            arg = re.sub(r"\(.*?\)", "", arg).strip(" ")
            msg = ":".join(splits[1:]).strip(" ")
            res[arg] = msg
        return res

    def get_return_msg(self, node):
        return super().get_return_msg(node)


class EpyTextParser(DocstringParser):
    def __init__(self):
        super().__init__()

    def get_help_msg(self, node):
        return super().get_help_msg(node)

    def get_arg_help_msg(self, node):
        return super().get_arg_help_msg(node)

    def get_return_msg(self, node):
        return super().get_return_msg(node)


class ReSTParser(DocstringParser):
    def __init__(self):
        super().__init__()

    def get_help_msg(self, node):
        return super().get_help_msg(node)

    def get_arg_help_msg(self, node):
        return super().get_arg_help_msg(node)

    def get_return_msg(self, node):
        return super().get_return_msg(node)


class NumpyDocParser(DocstringParser):
    def __init__(self):
        super().__init__()

    def get_help_msg(self, node):
        return super().get_help_msg(node)

    def get_arg_help_msg(self, node):
        return super().get_arg_help_msg(node)

    def get_return_msg(self, node):
        return super().get_return_msg(node)
