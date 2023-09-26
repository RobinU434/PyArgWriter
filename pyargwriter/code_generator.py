from argparse import ArgumentParser
import logging
from typing import Any, Dict, List, Type
from pyargwriter import Instances

class LineOfCode:
    def __init__(self, content: str, tab_level: int = 0) -> None:
        self._content: str = " " * (4 * tab_level) + content + "\n"

    def __repr__(self) -> str:
        return self._content
    
class Code:
    def __init__(self) -> None:
        self._file: List[LineOfCode] = []
        self._tab_level: int = 0
    
    def __repr__(self) -> str:
        result = ""
        for line in self._file:
            result += repr(line)

        return result
    
    def insert(self, content: List[LineOfCode] | LineOfCode, index: int) -> None:
        """insert given lines of code into self._file of class at given index

        Args:
            content (List[LineOfCode] | LineOfCode): Lines of code to insert 
            index (int): Where to insert the given content
        """
        first = self._file[:index]
        second = self._file[index:]

        # insert content
        if isinstance(content, list):
            concat = [*first, *content, *second]
        elif isinstance(content, LineOfCode):
            concat = [*first, content, *second]
        else:
            logging.error(f"Wrong type to insert into content. Allowed are List[LineOfCode] or LineOfCode. You provided: {type(content)}")
            return
        self._file = concat

    def append_line(self, content: str, tab_level: int = 0):
        self._file.append(LineOfCode(content=content, tab_level=tab_level))
        
    @property
    def file(self) -> List[LineOfCode]:
        return self._file
    

class Function(Code):
    def __init__(self, name: str, signature: Dict[str, Type] = {}, return_type: Type = None) -> None:
        super().__init__()

        self._name = name
        self._signature = signature
        self._return_type = return_type
        self._generate_header()

    def _generate_header(self):
        signature = str(self._signature).strip("{}").replace("'", "")
        
        first_line = f"def {self._name}({signature})"
        
        if self._return_type:
            first_line += f" -> {str(self._return_type)}"
        first_line += ":"

        self.append_line(content=first_line, tab_level=self._tab_level)

        self._tab_level += 1


class AddArguments(Function):
    """class adds function to add arguments function
    """
    def __init__(self, infix: str, arguments: List[Dict[str, Any]] = {}) -> None:
        self._check_infix(infix)
        name = f"add_{infix}_args"
        signature = {"parser": ArgumentParser.__name__}
        return_type = ArgumentParser.__name__
        super().__init__(name, signature, return_type)

        self._add_function(arguments)
    
    def _check_infix(self, infix: str) -> None:
        if " " in infix:
            raise ValueError(f"Insufficient character in infix found. ' ' not allowed in {infix}")
        if "-" in infix:
            raise ValueError(f"Insufficient character in infix found. '-' not allowed in {infix}")
    
    def _add_function(self, arguments: List[Dict[str,Any]]) -> None:
        for args_dict in arguments:
            self.append_line(content=f"parser.add_argument({dict2args(args_dict)})", tab_level=self._tab_level)
        
        self.append_line(content="return parser", tab_level=self._tab_level)


class SetupParser(Function):
    def __init__(self, commands: List[Dict[str,Any]]) -> None:
        name = "setup_parser"
        signature = {"parser": ArgumentParser.__name__}
        return_type = ArgumentParser.__name__
        super().__init__(name, signature, return_type)

        self._commands = commands

        self._add_command_parser()
        self._add_imports()
        self._add_return()
    
    def _add_imports(self):
        self.insert(LineOfCode(content="from argparse import ArgumentParser", tab_level=0), 0)

    def _add_command_parser(self) -> None:
        subparser_name = "command_subparser"
        self.append_line(content=f"{subparser_name} = parser.add_subparsers(dest='command', title='command')", tab_level=self._tab_level)
        
        for command in self._commands:
            parser_var_name = self._add_parser(subparser_name = subparser_name, **command)
            self.append_line(content=f"{parser_var_name} = add_{parser_var_name}_args({parser_var_name})", tab_level=self._tab_level)

    def _add_parser(self, subparser_name, name: str, help: str = "", args: List[Dict[str,Any]] = []) -> str:
        var_name = name.replace("-", "_")
        self.append_line(content=f"{var_name} = {subparser_name}.add_parser('{name}', help='{help}')", tab_level=self._tab_level)
        self._add_args(name_infix=var_name, args=args)
        return var_name

    def _add_args(self, name_infix: str, args: List[Dict[str, Any]]):
        args_func = AddArguments(infix=name_infix, arguments=args)
        self.insert(args_func.file, 0)

    def _add_return(self):
        self.append_line(content="return parser", tab_level=self._tab_level)


class Main(Code):
    def __init__(self) -> None:
        super().__init__()

        self._add_content()
    def _add_content(self):
        self.append_line(content="if __name__ == '__main__':", tab_level=self._tab_level)
        self._tab_level += 1

        self.append_line(content="parser = ArgumentParser(description='TODO: make it a variable')", tab_level=self._tab_level)
        self.append_line(content="parser = setup_parser(parser)", tab_level=self._tab_level)
        self.append_line(content="parser.parse_args()", tab_level=self._tab_level)




def dict2args(d: Dict[str,Any]) -> str:
    result = ""
    for key, value in d.items():
        if key == "type":
            value = f"{value}"
        else: 
            value = f"'{value}'"

        result += f"{key} = {value}, "

    return result


if __name__ == "__main__":
    data = {
        'commands': [
            {
                'name': 'command1',
                'help': 'Help for command1',
                'args': [
                    {
                        'dest': 'arg1',
                        'type': 'str',
                        'help': 'Help for arg1',
                        # 'required': True,
                        'default': None
                    },
                    {
                        'dest': 'arg2',
                        'type': 'int',
                        'help': 'Help for arg2',
                        # 'required': False,
                        'default': 0
                    }
                ]
            },
            {
                'name': 'command2',
                'help': 'Help for command2',
                'args': [
                    {
                        'dest': 'option1',
                        'type': 'bool',
                        'help': 'Help for option1',
                        # 'required': False,
                        'default': False
                    },
                    {
                        'dest': 'option2',
                        'type': 'str',
                        'help': 'Help for option2',
                        # 'required': True,
                        'default': 'default_value'
                    }
                ]
            },
            {
                'name': 'command3',
                'help': 'Help for command3',
                'args': [
                    {
                        'dest': 'arg3',
                        'type': 'list',
                        'help': 'Help for arg3',
                        # 'required': True,
                        'default': []
                    },
                    {
                        'dest': 'arg4',
                        'type': 'dict',
                        'help': 'Help for arg4',
                        # 'required': False,
                        'default': {}
                    }
                ]
            }
        ]
    }

    func = SetupParser(data['commands'])
    print(func)

    main = Main()
    print(main)
