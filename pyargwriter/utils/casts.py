from typing import Any, Dict, List

from pyargwriter.utils.structures import ArgumentStructure, CommandStructure


def dict2args(d: Dict[str,Any]) -> str:
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
            
        if key == "type":
            value = f"{value}"
        else: 
            value = f"'{value}'"

        result += f"{key} = {value}, "

    result = flags + result
    return result


def create_call_args(args: List[ArgumentStructure]) -> str:
    result = ""
    for arg in args:
        arg: ArgumentStructure
        result += f"{arg.dest} = args_dict['{arg.dest}']"
        result += ", "
    result = result[:-2]
    return result


def format_help(help: str) -> str:
    help = help.replace("'", '"')
    return help

