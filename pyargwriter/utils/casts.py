from typing import Any, Dict


def dict2args(d: Dict[str,Any]) -> str:
    result = ""
    for key, value in d.items():
        value = value.replace("_", "-")
        if key == "type":
            value = f"{value}"
        else: 
            value = f"'{value}'"

        result += f"{key} = {value}, "

    return result


def format_help(help: str) -> str:
    help = help.replace("'", '"')
    return help