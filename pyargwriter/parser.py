from argparse import ArgumentParser
from ast import AST, Module
import ast


def add_input_output_args(parser: ArgumentParser) -> ArgumentParser:
    parser.add_argument(
        "--input",
        nargs="+",
        type=str,
        help="Collection of paths to the files you want to generate the argument parser for.",
        required=True,
    )
    parser.add_argument(
        "--output",
        type=str,
        default=".",
        help="Relative path to directory where you want to save the generated files",
    )

    return parser


def setup_parser(parser: ArgumentParser) -> ArgumentParser:
    subparser = parser.add_subparsers(dest="command", title="command")

    gen_arg_pars_parser = subparser.add_parser(
        "generate-argparser",
        help="Generate parser.py which contains a setup_parser function to setup an appropriate parser.",
    )
    add_input_output_args(gen_arg_pars_parser)

    return parser


def generate_module_parser(tree: Module) -> ArgumentParser:
    module_docstring = ast.get_docstring(tree)
    first_line = module_docstring.split("\n")[0]
    name, description = first_line.split("-")
    parser = ArgumentParser(name, description=description)
    return parser


def generate_class_parser(tree: Module) -> ArgumentParser:
    pass


def generate_method_parser(tree: Module) -> ArgumentParser:
    pass


def parse_class(node: AST):
    class_name = node.name
    args = []
    for item in node.body:
        if isinstance(item, ast.FunctionDef) and item.name == "__init__":
            for arg in item.args.args[1:]:  # Exclude 'self' argument
                if isinstance(arg, ast.arg):
                    args.append(arg.arg)
    return class_name, args
