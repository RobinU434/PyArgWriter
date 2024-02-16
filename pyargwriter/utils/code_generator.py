from argparse import ArgumentParser
from copy import deepcopy
import logging
from typing import Any, Dict, List
from pyargwriter.utils.casts import create_call_args, dict2args, format_help
from pyargwriter.utils.code_abstracts import (
    Code,
    DefaultCase,
    Function,
    LineOfCode,
    Match,
    MatchCase,
)
from pyargwriter.utils.file_system import load_json, load_yaml
from pyargwriter.utils.structures import (
    ArgumentStructure,
    CommandStructure,
    ModuleStructure,
    ModuleStructures,
)


class AddArguments(Function):
    """Represents a class for adding arguments to a function.

    This class extends the Function class and is designed for generating functions that add arguments
    to an ArgumentParser instance. It automatically creates and appends the necessary code to add
    arguments to the parser function.

    Args:
        infix (str): The infix string used to construct the function name and as a part of the argument names.
        arguments (List[ArgumentStructure], optional): A list of ArgumentStructure objects representing the arguments to be added.

    Attributes:
        (inherited attributes from Function...)

    Methods:
        __init__(self, infix: str, arguments: List[ArgumentStructure] = {}) -> None:
            Initializes a new AddArguments instance with the specified infix and arguments.

        _check_infix(self, infix: str) -> None:
            Checks the validity of the provided infix string and raises an error if it contains spaces,
            dashes, or is not in lowercase.

        _add_function(self, arguments: List[ArgumentStructure]) -> None:
            Adds the code to add arguments to the ArgumentParser instance in the function.

    Example:
        >>> arguments = [ArgumentStructure(dest='input_file'), ArgumentStructure(dest='output_file')]
        >>> add_args_function = AddArguments("input", arguments)
        >>> print(add_args_function)
        def add_input_args(parser: ArgumentParser) -> ArgumentParser:
            parser.add_argument('--input-file', type = <class 'str'>, help = 'Path to input file')
            parser.add_argument('--output-file', type = <class 'str'>, help = 'Path to output file')
            return parser

    """

    def __init__(self, infix: str, arguments: List[ArgumentStructure] = {}) -> None:
        self._check_infix(infix)
        name = f"add_{infix}_args"
        signature = {"parser": ArgumentParser}
        return_type = ArgumentParser
        super().__init__(name, signature, return_type)

        self._add_function(arguments)

    def _check_infix(self, infix: str) -> None:
        """Check the validity of the provided infix string.

        Args:
            infix (str): The infix string to be checked.

        Raises:
            ValueError: If the infix contains spaces, dashes, or is not in lowercase.

        """
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
        """Add code to add arguments to the ArgumentParser instance in the function.

        Args:
            arguments (List[ArgumentStructure]): A list of ArgumentStructure objects representing the arguments to be added.

        """
        for arg in arguments:
            self.append(
                content=f"parser.add_argument({dict2args(vars(arg))})",
            )

        self.append(content="return parser")


class SetupCommandParser(Function):
    """Represents a function generator for setting up an ArgumentParser with subcommands.

    This class extends the Function class and is designed for generating functions that set up an ArgumentParser
    with subcommands based on a list of CommandStructure objects. It can optionally include imports for ArgumentParser.

    Args:
        module_name (str): The name of the module or command group.
        no_imports (bool, optional): If True, omit importing ArgumentParser; otherwise, include the import.

    Attributes:
        (inherited attributes from Function...)
        _commands (List[CommandStructure]): A list of CommandStructure objects representing the subcommands to be added.
        _imports (bool): Indicates whether ArgumentParser should be imported.

    Methods:
        generate_code(self, commands: List[CommandStructure]) -> Any:
            Generates the code to set up the ArgumentParser with subcommands, including imports (if enabled).

    Example:
        >>> commands = [CommandStructure(name='create', help='Create a new item'), CommandStructure(name='delete', help='Delete an existing item')]
        >>> setup_parser_function = SetupCommandParser('my_module', no_imports=True)
        >>> setup_parser_function.generate_code(commands)
        >>> print(setup_parser_function)
        def setup_my_module_parser(parser: ArgumentParser) -> ArgumentParser:
            command_subparser = parser.add_subparsers(dest='command', title='command')
            create = command_subparser.add_parser('create', help='Create a new item')
            delete = command_subparser.add_parser('delete', help='Delete an existing item')
            return parser

    """

    def __init__(self, module_name: str, no_imports: bool = False) -> None:
        name = f"setup_{module_name.lower()}_parser"
        signature = {"parser": ArgumentParser}
        return_type = ArgumentParser
        super().__init__(name, signature, return_type)

        self._commands: List[CommandStructure]
        self._imports = not no_imports

    def generate_code(self, commands: List[CommandStructure]) -> None:
        """Generates the code to set up the ArgumentParser with subcommands, including imports (if enabled).

        Args:
            commands (List[CommandStructure]): A list of CommandStructure objects representing the subcommands to be added.

        """
        self._commands = commands
        self._add_command_parser()
        if self._imports:
            self._add_imports()
        self._add_return()

    def _add_imports(self):
        """Add an import statement for ArgumentParser."""
        self.insert(
            LineOfCode(content="from argparse import ArgumentParser", tab_level=0), 0
        )

    def _add_command_parser(self) -> None:
        """Add code to set up the subcommand parser and add subcommands."""

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
        """Add code to set up a subcommand parser and add its arguments.

        Args:
            subparser_name (str): The name of the subparser.
            name (str): The name of the subcommand.
            help (str, optional): The help message for the subcommand.
            args (List[ArgumentStructure], optional): A list of ArgumentStructure objects representing the subcommand's arguments.

        Returns:
            str: The variable name of the subcommand parser.

        """
        var_name = name.replace("-", "_").lower()
        self.append(
            content=f"{var_name} = {subparser_name}.add_parser('{name.replace('_', '-')}', help='{format_help(help)}')",
        )
        self._add_args(name_infix=var_name, args=args)
        return var_name

    def _add_args(self, name_infix: str, args: List[ArgumentStructure]) -> None:
        """Add arguments to a subcommand parser.

        Args:
            name_infix (str): The infix used to construct variable names.
            args (List[ArgumentStructure]): A list of ArgumentStructure objects representing the subcommand's arguments.

        """
        args_func = AddArguments(infix=name_infix, arguments=args)
        self.insert(args_func, 0)

    def _add_return(self):
        """Add a return statement for the ArgumentParser."""
        self.append(content="return parser")


class SetupParser(Function):
    """Represents a function generator for setting up an ArgumentParser with subcommands for multiple modules.

    This class extends the Function class and is designed for generating functions that set up an ArgumentParser
    with subcommands for multiple modules based on ModuleStructures. It can handle the case of a single module or
    multiple modules with individual subparsers. Imports for ArgumentParser are included based on the number of modules.

    Args:
        None

    Attributes:
        (inherited attributes from Function...)

    Methods:
        generate_code(self, modules: ModuleStructures) -> None:
            Generates the code to set up the ArgumentParser with subcommands for multiple modules.
        from_yaml(self, yaml_file: str) -> None:
            Generates the code based on a YAML configuration file.
        from_json(self, json_file: str) -> None:
            Generates the code based on a JSON configuration file.

    Example:
        >>> modules = ModuleStructures(modules=[ModuleStructure(name='module1'), ModuleStructure(name='module2')])
        >>> setup_parser_function = SetupParser()
        >>> setup_parser_function.generate_code(modules)
        >>> print(setup_parser_function)
        def setup_parser(parser: ArgumentParser) -> ArgumentParser:
            module_subparser = parser.add_subparsers(dest='module', title='module')
            module1_parser = module_subparser.add_parser(name='module1', help='help of module1')
            setup_module1_parser = SetupCommandParser('module1', no_imports=False)
            setup_module1_parser.generate_code([])
            module1_parser = setup_module1_parser(module1_parser)
            module2_parser = module_subparser.add_parser(name='module2', help='help of module2')
            setup_module2_parser = SetupCommandParser('module2', no_imports=True)
            setup_module2_parser.generate_code([])
            module2_parser = setup_module2_parser(module2_parser)
            return parser

    """

    def __init__(self) -> None:
        name = "setup_parser"
        signature = {"parser": ArgumentParser}
        return_type = ArgumentParser
        super().__init__(name, signature, return_type)

    def generate_code(self, modules: ModuleStructures) -> None:
        """Generates the code to set up the ArgumentParser with subcommands for multiple modules.

        Args:
            modules (ModuleStructures): A ModuleStructures object containing information about the modules and their subcommands.

        """
        if len(modules) == 1:
            # only one class -> only command parser as setup_parser
            module: ModuleStructure = modules.modules[0]
            setup_command_parser = SetupCommandParser(module.name)
            module.add_args(module.args)
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
                    content=f"{module.name.lower()}_parser = module_subparser.add_parser(name='{module.name}', help='{module.help}')"
                )
                setup_command_parser = SetupCommandParser(
                    module.name, no_imports=bool(no_imports)
                )
                no_imports -= 1
                module.add_args(module.args)
                setup_command_parser.generate_code(module.commands)
                self.insert(setup_command_parser, 0)
                self.append(
                    content=f"{module.name.lower()}_parser = {setup_command_parser.name}({module.name.lower()}_parser)"
                )
            self.append(content="return parser")
        else:
            logging.info("No modules given. No setup parser code needs to be created")

    def from_yaml(self, yaml_file: str):
        """Generates the code based on a YAML configuration file.

        Args:
            yaml_file (str): The path to the YAML configuration file.

        """
        data = load_yaml(yaml_file)
        modules = ModuleStructures.from_dict(data)
        self.generate_code(modules)

    def from_json(self, json_file: str):
        """Generates the code based on a JSON configuration file.

        Args:
            json_file (str): The path to the JSON configuration file.

        """
        data = load_json(json_file)
        modules = ModuleStructures.from_dict(data)
        self.generate_code(modules)


class CreateParser(Function):
    def __init__(self) -> None:
        name = "create_parser"
        signature = {}
        return_type = ArgumentParser
        super().__init__(name, signature, return_type)

    def generate_code(self, modules: ModuleStructures):
        if len(modules) == 1:
            description = modules.modules[0].help
        elif len(modules) > 1:
            module_names = ", ".join(modules.names)
            description = f"Command-line interface for python modules: {module_names}"

        self.append(
            content=f"parser = ArgumentParser(description='{description}')",
        )
        self.append(content="parser = setup_parser(parser)")
        self.append(content="return parser")


class Execute(Function):
    """Creates execute function to execute program logic"""

    def __init__(self) -> None:
        name = "execute"
        signature = {"args": dict}
        return_type = bool
        super().__init__(name, signature, return_type)

    def generate_code(
        self,
        modules: ModuleStructures,
        project_root: str,
        setup_parser_file: str = "parser.py",
    ) -> None:
        self._insert_command_calling(modules)

        modules_to_import = modules.locations
        modules_to_import["setup_parser"] = setup_parser_file
        self._insert_imports(modules_to_import, project_root)

        self._tab_level = 0

    def _insert_command_calling(self, modules: ModuleStructures) -> None:
        """Adds logic to handle modules and commands.

        Args:
            data (ModuleStructures): A ModuleStructures object containing module and command information.
        """
        if len(modules) == 1:
            module: ModuleStructure = modules.modules[0]
            self.append(
                content=f"module = {module.name}({create_call_args(module.args)})"
            )

            # generate matches from commands
            match_case = self._generate_command_match_case(module.commands)
            self.append(match_case)
        elif len(modules) > 1:
            match_case = self._generate_module_match_case(modules.modules)
            self.append(match_case)
        else:
            logging.error("No given modules to process")

        self.append("return True")

    def _generate_command_match_case(
        self, commands: List[CommandStructure]
    ) -> MatchCase:
        """Generates match cases for commands.

        Args:
            commands (List[CommandStructure]): A list of CommandStructure objects representing the subcommands.

        Returns:
            MatchCase: A MatchCase object containing match cases for commands.
        """
        matches: List[Match] = []

        for command in commands:
            command: CommandStructure
            match_name = command.name.replace("_", "-")
            body = Code.from_str(
                code=f"module.{command.name}({create_call_args(command.args)})"
            )
            matches.append(Match(match_value=match_name, body=body))

        # add default case
        matches.append(DefaultCase(body="return False"))

        match_case = MatchCase(match_name="args['command']", matches=matches)
        return match_case

    def _generate_module_match_case(self, modules: List[ModuleStructure]) -> MatchCase:
        """Generates match cases for modules.

        Args:
            modules (List[ModuleStructure]): A list of ModuleStructure objects representing the modules.

        Returns:
            MatchCase: A MatchCase object containing match cases for modules.
        """
        matches: List[Match] = []

        for module in modules:
            module: ModuleStructure
            match_name = module.name
            body = Code.from_str(
                f"module = {module.name}({create_call_args(module.args)})"
            )
            body.append(self._generate_command_match_case(module.commands))
            matches.append(Match(match_value=match_name, body=body))

        # add default case
        matches.append(DefaultCase(body="return False"))

        match_cases = MatchCase(match_name="args['module']", matches=matches)
        return match_cases

    def _insert_imports(self, files: Dict[str, str], project_root: str) -> None:
        """Generates import statements for modules.

        Args:
            files (Dict[str, str]): A dictionary mapping module names to their file paths.
            project_root (str): what is the folder of the project main
        Returns:
            Code: A Code object containing import statements.
        """
        imports = Code()
        imports.append(content="from argparse import ArgumentParser")

        for module_name, path in files.items():
            path = (
                project_root.rstrip("/")
                + "/"
                + path.split(project_root)[-1].lstrip("/")
            )
            path = path.rstrip(".py")
            path = path.replace("/", ".")
            path = path.lstrip(".")
            imports.append(content=f"from {path} import {module_name}")
        self.insert(imports, 0)


class MainFunc(Function):
    """Represents the main function of a Python script that uses argparse for command-line arguments.

    This class extends the Function class and is designed to generate the code for the main function of a Python script that uses argparse for command-line argument parsing.

    Args:
        None

    Attributes:
        None

    Methods:
        generate_code(modules: ModuleStructures, setup_parser_file: str = "parser.py") -> Any: Generates the code for the main function.
        _add_content(): Adds the main function's content.
        _generate_imports(files: Dict[str, str]) -> Code: Generates import statements for modules.
        _add_module_logic(data: ModuleStructures): Adds the logic to handle modules and commands.
        _generate_command_match_case(commands: List[CommandStructure]) -> MatchCase: Generates match cases for commands.
        _generate_module_match_case(modules: List[ModuleStructure]) -> MatchCase: Generates match cases for modules.

    Example:
        >>> main_function = MainFunc()
        >>> print(main_function)
        def main():
            parser = ArgumentParser(description='description for ArgumentParser')
            parser = setup_parser(parser)
            args = parser.parse_args()
            args_dict = vars(args)
            # (module and command logic)
    """

    def __init__(self) -> None:
        """_summary_

        Args:
            setup_parser_file (str): relative path to file with setup parser functionalities
        """
        name = "main"
        signature = {}
        return_type = None
        super().__init__(name, signature, return_type)

    def generate_code(self) -> None:
        """Generates the code for the main function.

        Args:
            modules (ModuleStructures): A ModuleStructures object containing module and command information.
            setup_parser_file (str, optional): The relative path to the setup parser file. Defaults to "parser.py".

        Returns:
            Any: Generated code for the main function.
        """
        # convert module names in comprehensive string

        self.append(content="parser = create_parser()")
        # self.append_line(content="raise ValueError", tab_level=1)
        self.append(content="args = parser.parse_args()")
        self.append(content="args_dict = vars(args)")

        self.append(content="if not execute(args_dict):")
        self._tab_level += 1
        self.append(content="parser.print_usage()")
        self._tab_level = 0


class MainCaller(Code):
    """Represents a code block for calling the `main()` function if the script is executed as the main program.

    This class extends the Code class and is designed to generate code that calls the `main()` function if the script is executed as the main program.

    Args:
        None

    Attributes:
        None

    Methods:
        None

    Example:
        >>> main_caller = MainCaller()
        >>> print(main_caller)
        if __name__ == '__main__':
            main()
    """

    def __init__(self) -> None:
        super().__init__()
        self._add_content()

    def _add_content(self):
        self.append(content="if __name__ == '__main__':")
        self._tab_level += 1
        self.append(content="main()")


class CodeGenerator:
    """Generates Python code for creating argparse-based command-line parsers.

    This class provides methods to generate Python code for creating argparse-based command-line parsers, including the setup parser, main function, and main caller.

    Args:
        None

    Attributes:
        _setup_parser (SetupParser): An instance of the SetupParser class for generating setup parser code.
        _main_func (MainFunc): An instance of the MainFunc class for generating main function code.
        _main_caller (MainCaller): An instance of the MainCaller class for generating main caller code.

    Methods:
        from_dict(modules: List[Dict[str, Any]], parser_file: str) -> None: Generates code based on a list of module dictionaries and a parser file name.
        from_yaml(yaml_file: str, parser_file: str): Generates code from a YAML file and a parser file name.
        from_json(json_file: str, parser_file: str): Generates code from a JSON file and a parser file name.
        write(setup_parser_path: str, main_path: str, force: bool = False): Writes the generated code to specified files.

    Example:
        >>> generator = CodeGenerator()
        >>> modules_data = [{"name": "module1", "commands": [...]}, {"name": "module2", "commands": [...]}]
        >>> parser_file = "my_parser.py"
        >>> generator.from_dict(modules_data, parser_file)
        >>> generator.write("setup_parser.py", "main.py")
    """

    def __init__(self) -> None:
        self._setup_parser = SetupParser()
        self._create_parser = CreateParser()
        self._execute = Execute()
        self._main_func = MainFunc()
        self._main_caller = MainCaller()

    def from_dict(self, modules: List[Dict[str, Any]], parser_file: str) -> None:
        """Generates code based on a list of module dictionaries and a parser file name.

        Args:
            modules (List[Dict[str, Any]]): A list of dictionaries representing the module structure.
            parser_file (str): The path to the future parser file.
        """
        modules = ModuleStructures.from_dict(modules)

        self._setup_parser.generate_code(deepcopy(modules))

        project_root = parser_file.split("/")[0]
        self._execute.generate_code(
            modules=deepcopy(modules),
            project_root=project_root,
            setup_parser_file=parser_file,
        )

        self._create_parser.generate_code(deepcopy(modules))
        self._execute.append(self._create_parser)

        self._main_func.generate_code()
        self._main_func.insert(self._execute, 0)

        self._main_func.append(self._main_caller)

    def from_yaml(self, yaml_file: str, parser_file: str) -> None:
        """Generates code from a YAML file and a parser file name.

        Args:
            yaml_file (str): The path to the YAML file containing module structure data.
            parser_file (str): The path to the future parser file.

        """
        data = load_yaml(yaml_file)
        self.from_dict(data, parser_file)

    def from_json(self, json_file: str, parser_file: str) -> None:
        """Generates code from a JSON file and a parser file name.

        Args:
            json_file (str): The path to the JSON file containing module structure data.
            parser_file (str): The path to the future parser file.

        """
        data = load_json(json_file)
        self.from_dict(data, parser_file)

    def write(
        self, setup_parser_path: str, main_path: str, force: bool = False
    ) -> None:
        """Generates code from a JSON file and a parser file name.

        Args:
            json_file (str): The path to the JSON file containing module structure data.
            parser_file (str): The path to the future parser file.
        """
        if force:
            self._setup_parser.write_force(path=setup_parser_path)
            self._main_func.write_force(path=main_path)
        else:
            self._setup_parser.write(path=setup_parser_path)
            self._main_func.write(path=main_path)
