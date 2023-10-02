from argparse import ArgumentParser
import logging
from types import NoneType
from typing import Any, Dict, List, Type
from pyargwriter.utils.casts import dict2args, format_help
from pyargwriter.utils.code_abstracts import (
    Code,
    Function,
    LineOfCode,
    Match,
    MatchCase,
)
from pyargwriter.utils.file_system import check_file_exists, load_json, load_yaml
from pyargwriter.utils.structures import (
    ArgumentStructure,
    CommandStructure,
    ModuleStructure,
    ModuleStructures,
)


class AddArguments(Function):
    """class adds function to add arguments function"""

    def __init__(self, infix: str, arguments: List[ArgumentStructure] = {}) -> None:
        self._check_infix(infix)
        name = f"add_{infix}_args"
        signature = {"parser": ArgumentParser.__name__}
        return_type = ArgumentParser.__name__
        super().__init__(name, signature, return_type)

        self._add_function(arguments)

    def _check_infix(self, infix: str) -> None:
        if " " in infix:
            raise ValueError(
                f"Insufficient character in infix found. ' ' not allowed in {infix}"
            )
        if "-" in infix:
            raise ValueError(
                f"Insufficient character in infix found. '-' not allowed in {infix}"
            )
        if infix != infix.lower():
            raise ValueError("infix is not correctly formatted")

    def _add_function(self, arguments: List[ArgumentStructure]) -> None:
        for arg in arguments:
            self.append(
                content=f"parser.add_argument({dict2args(vars(arg))})",
            )

        self.append(content="return parser")


class SetupCommandParser(Function):
    def __init__(self, module_name: str, no_imports: bool = False) -> None:
        name = f"setup_{module_name.lower()}_parser"
        signature = {"parser": ArgumentParser.__name__}
        return_type = ArgumentParser.__name__
        super().__init__(name, signature, return_type)

        self._commands: List[CommandStructure]
        self._imports = not no_imports

    def generate_code(self, commands: List[CommandStructure]) -> Any:
        self._commands = commands
        self._add_command_parser()
        if self._imports:
            self._add_imports()
        self._add_return()

    def _add_imports(self):
        self.insert(
            LineOfCode(content="from argparse import ArgumentParser", tab_level=0), 0
        )

    def _add_command_parser(self) -> None:
        subparser_name = "command_subparser"
        self.append(
            content=f"{subparser_name} = parser.add_subparsers(dest='command', title='command')",
        )

        for command in self._commands:
            parser_var_name = self._add_parser(
                subparser_name=subparser_name, **vars(command)
            )
            self.append(
                content=f"{parser_var_name} = add_{parser_var_name}_args({parser_var_name})",
            )

    def _add_parser(
        self,
        subparser_name,
        name: str,
        help: str = "",
        args: List[ArgumentStructure] = [],
    ) -> str:
        var_name = name.replace("-", "_").lower()
        self.append(
            content=f"{var_name} = {subparser_name}.add_parser('{name.replace('_', '-')}', help='{format_help(help)}')",
        )
        self._add_args(name_infix=var_name, args=args)
        return var_name

    def _add_args(self, name_infix: str, args: List[ArgumentStructure]):
        args_func = AddArguments(infix=name_infix, arguments=args)
        self.insert(args_func, 0)

    def _add_return(self):
        self.append(content="return parser")


class SetupParser(Function):
    def __init__(self) -> None:
        name = "setup_parser"
        signature = {"parser": ArgumentParser.__name__}
        return_type = ArgumentParser.__name__
        super().__init__(name, signature, return_type)

    def generate_code(self, modules: ModuleStructures) -> Any:
        if len(modules) == 1:
            # only one class -> only command parser as setup_parser
            module: ModuleStructure = modules.modules[0]
            setup_command_parser = SetupCommandParser(module.name)
            setup_command_parser.generate_code(module.commands)
            self.insert(setup_command_parser, 0)
            self.append(content=f"parser = {setup_command_parser.name}(parser)")
            self.append(content="return parser")

        elif len(modules) > 1:
            # multiple classes -> unify multiple parser architectures
            self.append(
                content="module_subparser = parser.add_subparsers(dest='module', title='module')"
            )
            no_imports = len(modules) - 1
            for module in modules.modules:
                self.append(
                    content=f"{module.name.lower()}_parser = module_subparser.add_parser(name='{module.name}', help='TODO')"
                )
                setup_command_parser = SetupCommandParser(
                    module.name, no_imports=bool(no_imports)
                )
                no_imports -= 1
                setup_command_parser.generate_code(module.commands)
                self.insert(setup_command_parser, 0)
                self.append(
                    content=f"{module.name.lower()}_parser = {setup_command_parser.name}({module.name.lower()}_parser)"
                )
            self.append(content="return parser")
        else:
            logging.info("No modules given. No setup parser code needs to be created")

    def from_yaml(self, yaml_file: str):
        data = load_yaml(yaml_file)
        modules = ModuleStructures.from_dict(data)
        self.generate_code(modules)

    def from_json(self, json_file: str):
        data = load_json(json_file)
        modules = ModuleStructures.from_dict(data)
        self.generate_code(modules)


class MainCaller(Code):
    def __init__(self) -> None:
        super().__init__()
        self._add_content()

    def _add_content(self):
        self.append(content="if __name__ == '__main__':")
        self._tab_level += 1
        self.append(content="main()")


class MainFunc(Function):
    def __init__(self) -> None:
        """_summary_

        Args:
            setup_parser_file (str): relative path to file with setup parser functionalities
        """
        name = "main"
        signature = {}
        return_type = None
        super().__init__(name, signature, return_type)

    def generate_code(
        self, modules: ModuleStructures, setup_parser_file: str = "parser.py"
    ) -> Any:
        self._add_content()
        imports = self._generate_imports(setup_parser_file)
        self.insert(imports, 0)
        self._add_module_logic(modules)

    def _add_content(self):
        self.append(
            content="parser = ArgumentParser(description='TODO: make it a variable')",
        )
        self.append(content="parser = setup_parser(parser)")
        # self.append_line(content="raise ValueError", tab_level=1)
        self.append(content="args = parser.parse_args()")
        self.append(content="args_dict = vars(args)")

    def _generate_imports(self, file: str) -> Code:
        imports = Code()
        imports.append(content="from argparse import ArgumentParser")
        file = file.rstrip(".py")
        file = file.replace("/", ".")
        imports.append(content=f"from {file} import setup_parser")
        return imports

    def _add_module_logic(self, data: ModuleStructures):
        if len(data) == 1:
            module: ModuleStructure = data.modules[0]
            self.append(content=f"module = {module.name}(**args_dict)")

            # generate matches from commands
            match_case = self._generate_command_match_case(module.commands)
            self.append(match_case)
        elif len(data) > 1:
            match_case = self._generate_module_match_case(data.modules)
            self.append(match_case)
        else:
            logging.error("No given modules to process")
        print(len(self))

    def _generate_command_match_case(
        self, commands: List[CommandStructure]
    ) -> MatchCase:
        matches: List[Match] = []

        for command in commands:
            command: CommandStructure
            match_name = command.name
            body = Code.from_str(code=f"module.{command.name}(**args_dict)")
            matches.append(Match(match_value=match_name, body=body))

        match_case = MatchCase(match_name="args_dict['command']", matches=matches)
        return match_case

    def _generate_module_match_case(self, modules: List[ModuleStructure]) -> MatchCase:
        matches: List[Match] = []

        for module in modules:
            module: ModuleStructure
            match_name = module.name
            body = Code.from_str(f"module = {module.name}(**args_dict)")
            body.append(self._generate_command_match_case(module.commands))
            matches.append(Match(match_value=match_name.replace("_", "-"), body=body))
            
        match_cases = MatchCase(match_name="args_dict['module']", matches=matches)
        return match_cases


class CodeGenerator:
    def __init__(self) -> None:
        self._setup_parser = SetupParser()
        self._main_func = MainFunc()
        self._main_caller = MainCaller()

    def from_dict(self, modules: List[Dict[str, Any]], parser_file: str) -> None:
        """_summary_

        Args:
            modules (List[Dict[str, Any]]): parser structure
            parser_file (str): path to future parser file
        """
        modules = ModuleStructures.from_dict(modules)
        self._setup_parser.generate_code(modules)
        self._main_func.generate_code(modules, parser_file)
        self._main_func.insert(self._main_caller, len(self._main_func))

    def from_yaml(self, yaml_file: str, parser_file: str):
        data = load_yaml(yaml_file)
        self.from_dict(data, parser_file)

    def from_json(self, json_file: str, parser_file: str):
        data = load_json(json_file)
        self.from_dict(data, parser_file)

    def write(self, setup_parser_path: str, main_path: str, force: bool = False):
        if force:
            self._setup_parser.write_force(path=setup_parser_path)
            self._main_func.write_force(path=main_path)
        else:
            self._setup_parser.write(path=setup_parser_path)
            self._main_func.write(path=main_path)
