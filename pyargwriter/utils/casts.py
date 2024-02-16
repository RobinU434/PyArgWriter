from typing import Any, Dict, List

from pyargwriter.utils.structures import ArgumentStructure


def dict2args(d: Dict[str, Any]) -> str:
    """Convert a dictionary into a string of keyword arguments.

    This function takes a dictionary and converts it into a string representation of keyword arguments
    in the format 'key = value'. It is primarily used for generating arguments for function calls.

    Args:
        d (Dict[str, Any]): The dictionary to be converted into keyword arguments.

    Returns:
        str: A string of keyword arguments in the format 'key = value'.

    Example:
        >>> d = {'name_or_flags': 'input_file', 'type': str, 'help': 'Path to input file'}
        >>> dict2args(d)
        "'--input-file', type = <class 'str'>, help = 'Path to input file'"

    """
    result = ""
    flags = ""
    for key, value in d.items():
        if key == "name_or_flags":
            value = value.replace("_", "-")
            # make value to flag
            flag = "--" + value
            flag = f"'{flag}'"
            flags += flag
            flags += ", "
            continue

        elif key == "type":
            if value == "bool" and "nargs" not in d.keys():
                # no action="store_true" for list arguments
                result += "action = 'store_true', "
                continue
            value = f"{value}"

        elif key == "default":
            if isinstance(value, bool):
                # no default value for action="store_true"
                continue
            elif isinstance(value, list):
                # no '' around a default list element
                value = str(value)
            elif isinstance(value, str):
                value = f"'{value}'"
        else:
            value = f"'{value}'"

        result += f"{key} = {value}, "

    result = flags + result
    return result


def create_call_args(args: List[ArgumentStructure]) -> str:
    """Create function call arguments from a list of ArgumentStructure objects.

    This function takes a list of ArgumentStructure objects and generates function call arguments
    by extracting the 'dest' attribute from each ArgumentStructure.

    Args:
        args (List[ArgumentStructure]): A list of ArgumentStructure objects.

    Returns:
        str: A string of function call arguments.

    Example:
        >>> args = [ArgumentStructure(dest='input_file'), ArgumentStructure(dest='output_file')]
        >>> create_call_args(args)
        'input_file = args_dict[\'input_file\'], output_file = args_dict[\'output_file\']'

    """
    result = ""
    for arg in args:
        arg: ArgumentStructure
        result += f"{arg.dest} = args['{arg.dest}']"
        result += ", "
    result = result[:-2]
    return result


def format_help(help: str) -> str:
    """Format help text for better readability.

    This function takes a help string and replaces single quotes with double quotes to ensure
    consistent formatting of help text.

    Args:
        help (str): The help text to be formatted.

    Returns:
        str: The formatted help text with double quotes.

    Example:
        >>> help_text = "This is an example help text with 'single quotes'."
        >>> format_help(help_text)
        "This is an example help text with \"single quotes\"."

    """
    help = help.replace("'", '"')
    return help
