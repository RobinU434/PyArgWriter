from argparse import ArgumentParser


def add_general_args(parser: ArgumentParser) -> ArgumentParser:
    """Add general arguments to the given ArgumentParser.

    Args:
        parser (ArgumentParser): The ArgumentParser to which general arguments will be added.

    Returns:
        ArgumentParser: The modified ArgumentParser.
    """
    parser.add_argument(
        "--log-level",
        choices=["DEBUG", "INFO", "WARN", "ERROR", "CRITICAL"],
        default="WARN",
        help="Sets log level for command execution.",
    )
    return parser


def add_formatter_args(parser: ArgumentParser) -> ArgumentParser:
    """Add formatter-related arguments to the given ArgumentParser.

    Args:
        parser (ArgumentParser): The ArgumentParser to which formatter-related arguments will be added.

    Returns:
        ArgumentParser: The modified ArgumentParser.
    """
    parser.add_argument(
        "--pretty",
        "-p",
        action="store_true",
        help="If flag is set. The code will be formatted with Black.",
    )
    return parser


def add_parser_args(parser: ArgumentParser) -> ArgumentParser:
    """Add arguments for parsing code to the given ArgumentParser.

    Args:
        parser (ArgumentParser): The ArgumentParser to which parsing-related arguments will be added.

    Returns:
        ArgumentParser: The modified ArgumentParser.
    """
    parser.add_argument(
        "--input",
        dest="files",
        nargs="+",
        type=str,
        help="Collection of paths to the files you want to generate the argument parser for.",
        required=True,
    )
    parser.add_argument(
        "--output",
        type=str,
        default=".",
        help="Path to file where to store the structural information",
    )
    parser = add_general_args(parser)
    return parser


def add_writer_args(parser: ArgumentParser) -> ArgumentParser:
    """Add arguments for writing code to the given ArgumentParser.

    Args:
        parser (ArgumentParser): The ArgumentParser to which writing-related arguments will be added.

    Returns:
        ArgumentParser: The modified ArgumentParser.
    """
    parser.add_argument(
        "--input",
        dest="file",
        type=str,
        help="Collection of paths to files with structural information to generate the parser from. ",
        required=True,
    )
    parser.add_argument(
        "--output",
        type=str,
        default=".",
        help="Relative path to directory where you want to save the generated files",
    )
    parser = add_formatter_args(parser)
    parser = add_general_args(parser)

    parser.add_argument(
        "--force",
        "-f",
        action="store_true",
        help="Set this argument to force file overwrite.",
    )
    return parser


def add_generate_parser_args(parser: ArgumentParser) -> ArgumentParser:
    """Add arguments for generating an argument parser to the given ArgumentParser.

    Args:
        parser (ArgumentParser): The ArgumentParser to which generation-related arguments will be added.

    Returns:
        ArgumentParser: The modified ArgumentParser.
    """
    parser.add_argument(
        "--input",
        dest="files",
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
    parser = add_formatter_args(parser)
    parser = add_general_args(parser)

    parser.add_argument(
        "--force",
        "-f",
        action="store_true",
        help="Set this argument to force file overwrite.",
    )
    return parser


def setup_parser(parser: ArgumentParser) -> ArgumentParser:
    """Set up the main ArgumentParser with subparsers for different commands.

    Args:
        parser (ArgumentParser): The main ArgumentParser.

    Returns:
        ArgumentParser: The main ArgumentParser with subparsers.
    """
    subparser = parser.add_subparsers(dest="command", title="command")

    parse_code_parser = subparser.add_parser(
        "parse-code",
        help="Parse given files and create yaml structure with structural parser information",
    )
    parse_code_parser = add_parser_args(parse_code_parser)

    write_code_parser = subparser.add_parser(
        "write-code",
        help="Read given parser yaml structure and create argument parser python code",
    )
    write_code_parser = add_writer_args(write_code_parser)

    gen_arg_pars_parser = subparser.add_parser(
        "generate-argparser",
        help="Generate parser.py which contains a setup_parser function to setup an appropriate parser.",
    )
    gen_arg_pars_parser = add_generate_parser_args(gen_arg_pars_parser)

    return parser
