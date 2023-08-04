

from typing import List
from ast import Module
import ast
import argparse
from argparse import ArgumentParser

from pyargwriter.parser import generate_module_parser

class ArgParsWriter:
    def __init__(self, input: List[str], output: str, **kwargs) -> None:
        self._input = input
        """List of files where to generate the argument parser from"""
        self._output = output
        """directory where to store the generated code"""

        self._parser: argparse.ArgumentParser

    @staticmethod
    def _load_file_tree(file_path: str) -> Module:
        with open(file_path, 'r') as file:
            tree = ast.parse(file.read())
        return tree

    
    def _generate_class_parser(tree: Module) -> ArgumentParser:
        pass

    def _generate_method_parser(tree: Module) -> ArgumentParser:
        pass


    def generate_parser(self):
        tree = self._load_file_tree(self._input[0])
        parser = generate_module_parser(tree)
        
        class_parsers = {}
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):

                class_name, args = parse_class(node)
                print(class_name, args)
                class_parser = generate_class_parser(class_name, args)
                method_parsers = {}
        """
                for inner_node in node.body:
                    if isinstance(inner_node, ast.FunctionDef):
                        method_name, args = parse_method(inner_node)
                        method_parser = generate_method_parser(method_name, args)
                        method_parsers[method_name] = method_parser
                class_parsers[class_name] = (class_parser, method_parsers)
        return class_parsers"""


def generate_parser_functions_code(class_parsers):
    code = []
    for class_name, (class_parser, method_parsers) in class_parsers.items():
        class_code = f"{class_name}_parser = {generate_class_parser(class_name).__name__}"
        code.append(class_code)

        for method_name, method_parser in method_parsers.items():
            method_code = f"{method_name}_parser = {generate_method_parser(method_name).__name__}"
            code.append(method_code)

    return "\n".join(code)

def dump_parser_code_to_file(code, output_file="parser.py"):
    with open(output_file, "w") as file:
        file.write(code).i765s14d

def parse_class(node):
    class_name = node.name
    args = []
    for item in node.body:
        if isinstance(item, ast.FunctionDef) and item.name == "__init__":
            for arg in item.args.args[1:]:  # Exclude 'self' argument
                if isinstance(arg, ast.arg):
                    args.append(arg.arg)
    return class_name, args

def parse_method(node):
    method_name = node.name
    args = []
    for arg in node.args.args:
        if isinstance(arg, ast.arg):
            args.append(arg.arg)
    return method_name, args

def generate_class_parser(class_name, args):
    def create_class_parser():
        parser = argparse.ArgumentParser(description=f'Parser for {class_name}')
        # Add arguments to the parser based on the class's __init__ parameters
        for arg in args:
            parser.add_argument(arg)
        return parser
    return create_class_parser

def generate_method_parser(method_name, args):
    def create_method_parser():
        parser = argparse.ArgumentParser(description=f'Parser for {method_name}')
        # Add arguments to the parser based on the method's parameters
        for arg in args:
            parser.add_argument(arg)
        return parser
    return create_method_parser

def process_file(file_path):
    with open(file_path, 'r') as file:
        tree = ast.parse(file.read())
        class_parsers = {}
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                class_name, args = parse_class(node)
                class_parser = generate_class_parser(class_name, args)
                method_parsers = {}
                for inner_node in node.body:
                    if isinstance(inner_node, ast.FunctionDef):
                        method_name, args = parse_method(inner_node)
                        method_parser = generate_method_parser(method_name, args)
                        method_parsers[method_name] = method_parser
                class_parsers[class_name] = (class_parser, method_parsers)
        return class_parsers

if __name__ == "__main__":
    file_path = "path/to/your/python/file.py"
    class_parsers = process_file(file_path)
    
    # Example: Access and use the generated parsers
    class_name = "YourClassName"
    method_name = "your_method"
    
    if class_name in class_parsers:
        class_parser, method_parsers = class_parsers[class_name]
        class_args = class_parser()
        print(class_args.parse_args())
        
        if method_name in method_parsers:
            method_parser = method_parsers[method_name]
            method_args = method_parser()
            print(method_args.parse_args())
