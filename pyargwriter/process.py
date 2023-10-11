import logging
from typing import Any, Dict, List
from ast import Module
import ast
import argparse
from argparse import ArgumentParser
from pyargwriter.utils.code_generator import CodeGenerator
from pyargwriter.utils.code_parser import CodeParser
from pyargwriter.utils.decorator import overwrite_protection
from pyargwriter.utils.file_system import (
    check_file_exists,
    create_directory,
    create_file,
)
from pyargwriter.utils.formatter import BlackFormatter


class ArgParseWriter:
    def __init__(self, force: bool = False, **kwargs) -> None:
        self._force = force

        self._parser = CodeParser()
        self._generator = CodeGenerator()

        self._formatter = BlackFormatter()

        self._arg_parse_structure: Dict[str, Any]

    def parse_code(self, files: List[str], output: str, **kwargs):
        for file in files:
            tree = self._load_file_tree(file)
            self._parser.parse_tree(tree, file)

        self._arg_parse_structure = self._parser.modules

        # how to return values
        if output == ".":
            print(repr(self._arg_parse_structure))
        elif output is None:
            return
        else:
            self._parser.write(output)

    def write_code(self, file: str, output: str, pretty: bool = False, **kwargs):
        file_type = file.split(".")[-1]
        match file_type:
            case "yaml":
                generator_method = self._generator.from_yaml
            case "yml":
                generator_method = self._generator.from_yaml
            case "yaml":
                generator_method = self._generator.from_json

        output = output.rstrip("/")
        generator_method(file, output + "/utils/parser.py")

        create_directory(output + "/utils")
        self._generator.write(
            setup_parser_path=output + "/utils/parser.py",
            main_path=output + "/__main__.py",
            force=self._force,
        )

        # create __init__.py ?
        init_path = output + "/__init__.py"
        self._create_init(path=init_path)
        # if not check_file_exists(output + "/__init__.py"):
        #     create_init = input(f"No __init__.py in {output} found. Create one? [Y, n]:")
        #     if create_init.lower() in ["", "y"]:
        #         create_file(output  + "/__init__.py")

        if pretty:
            self._format_code(output)

    def generate_parser(
        self,
        files: List[str],
        output: str,
        pretty: bool = False,
        **kwargs,
    ):
        self.parse_code(files, None)

        output = output.rstrip("/")
        self._generator.from_dict(
            self._arg_parse_structure.to_dict(), output + "/utils/parser.py"
        )

        create_directory(output + "/utils")
        self._generator.write(
            setup_parser_path=output + "/utils/parser.py",
            main_path=output + "/__main__.py",
            force=self._force,
        )

        # create __init__.py ?
        init_path = output + "/__init__.py"
        self._create_init(path=init_path)
        # if not check_file_exists(output + "/__init__.py"):
        #     create_init = input(f"No __init__.py in {output} found. Create one? [Y, n]:")
        #     if create_init.lower() in ["", "y"]:
        #         create_file(output  + "/__init__.py")

        if pretty:
            self._format_code(output)

    def _format_code(
        self,
        *files,
    ):
        logging.info(f"Format code with {type(self._formatter).__name__}")
        self._formatter.format(files)

    def _create_init(self, path):
        if self._force:
            create_file(path)
        else:

            @overwrite_protection
            def wrapper(path):
                create_file(path)

            wrapper(path=path)

    @staticmethod
    def _load_file_tree(file_path: str) -> Module:
        with open(file_path, "r") as file:
            tree = ast.parse(file.read())
        return tree
