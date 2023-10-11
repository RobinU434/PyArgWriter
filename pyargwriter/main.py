import sys
from argparse import ArgumentParser
from typing import Any, Dict

from pyargwriter.process import ArgParseWriter
from pyargwriter.utils.log_level import set_log_level
from pyargwriter.utils.parser import setup_parser


def create_parser() -> ArgumentParser:
    parser = ArgumentParser(
        description="PyArgWriter: Python Argument Parser Setup Writer",
        epilog="Automatically generates ArgumentParser setups for Python classes and their methods.",
    )
    parser = setup_parser(parser)
    return parser


def execute(args: Dict[str, Any]):
    arg_pars_writer = ArgParseWriter(**args)
    if args["command"] == "parse-code":
        arg_pars_writer.parse_code(**args)
    elif args["command"] == "write-code":
        arg_pars_writer.write_code(**args)
    elif args["command"] == "generate-argparser":
        arg_pars_writer.generate_parser(**args)
    else:
        raise KeyError("No fitting value behind args['command']")


def main():
    """Main entry point for the PyArgWriter script.

    This function sets up the ArgumentParser, parses command-line arguments,
    initializes the ArgParseWriter, and calls the appropriate method based on
    the provided command.

    """
    parser = create_parser()
    args = vars(parser.parse_args())
    set_log_level(args["log_level"])

    try:
        execute(args)
    except KeyError:
        parser.print_usage()


