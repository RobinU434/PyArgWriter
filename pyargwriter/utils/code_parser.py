from ast import ClassDef, FunctionDef, Module
import ast
import logging
from typing import List, Tuple

from pyargwriter.utils.file_system import write_json, write_yaml
from pyargwriter.utils.structures import (
    ArgumentStructure,
    CommandStructure,
    ModuleStructure,
    ModuleStructures,
)


class CodeParser:
    """A parser for analyzing Python code and extracting structured information.

    This class is designed to parse Python code and extract structured information
    about classes, methods, and their associated arguments and documentation.

    Attributes:
        modules (ModuleStructures): A collection of ModuleStructure objects.

    Methods:
        parse_tree(self, tree: Module, file: str) -> None:
            Parse the Abstract Syntax Tree (AST) of a Python module and extract structured information.

        write(self, path: str) -> None:
            Write the extracted structured information to a file in YAML or JSON format.

    Properties:
        module_serialized: A list of dictionaries representing serialized module information.

    """

    def __init__(self) -> None:
        self.modules = ModuleStructures()

    def __repr__(self) -> str:
        """Return a string representation of the parsed modules.

        Returns:
            str: A string representation of the parsed modules.
        """
        result = "["
        for module in self.modules.modules:
            result += repr(module)
            result += ",\n"
        result = result.rstrip(",\n")
        result += "]"
        return result

    @property
    def module_serialized(self):
        """Serialize the module information as a list of dictionaries.

        Returns:
            List[dict]: A list of dictionaries representing serialized module information.
        """
        result = []
        for module in self.modules.modules:
            result.append(module.to_dict())
        return result

    def write(self, path: str):
        """Write the extracted structured information to a file in YAML or JSON format.

        Args:
            path (str): The path to the output file.

        """
        if "." not in path:
            logging.error(
                "No file specified but directory specified. Please provide a file as output."
            )
            return

        file_type = path.split(".")[-1]
        match file_type:
            case "yaml":
                write_func = write_yaml
            case "yml":
                write_func = write_yaml
            case "json":
                write_func = write_json
            case _:
                msg = f"Not implemented write method for file type {file_type}"
                logging.error(msg)

        write_func(self.modules.to_dict(), path)

    def _get_class_signature(self, node) -> Tuple[str, List[ArgumentStructure], str]:
        """Get the signature (name and arguments) of a class.

        Args:
            node: The AST node representing the class.

        Returns:
            Tuple[str, List[ArgumentStructure], str]: A tuple containing the class name, its arguments and a short explanation.
        """
        class_name = node.name
        args = []
        for item in node.body:
            if isinstance(item, ast.FunctionDef) and item.name == "__init__":
                args = self._get_arguments(item)

        help_message = ast.get_docstring(node).split("\n")[0]
        return class_name, args, help_message

    def _get_arguments(self, func: FunctionDef) -> List[ArgumentStructure]:
        """Get the arguments of a function.

        Args:
            func (FunctionDef): The AST node representing the function.

        Returns:
            List[ArgumentStructure]: A list of ArgumentStructure objects representing function arguments.
        """
        num_args = len(func.args.args)
        if "staticmethod" not in [decorator.id for decorator in func.decorator_list]:
            num_args -= 1
        helps = self._get_help_msgs(func, num_args)

        # add defaults
        defaults = [None] * num_args
        if len(func.args.defaults):
            defaults[-len(func.args.defaults) :] = func.args.defaults  # noqa: E203

        arguments = []
        for arg, help_message, default in zip(
            func.args.args[-num_args:], helps, defaults
        ):
            argument = ArgumentStructure()
            argument.dest = arg.arg
            argument.name_or_flags = arg.arg
            argument.help = help_message

            if arg.annotation:
                if isinstance(arg.annotation, ast.Name):
                    argument.type = eval(arg.annotation.id)
                elif isinstance(arg.annotation, ast.Subscript):
                    # argument type is a list of some values
                    # logging.warning(
                    #     "List annotation automatically set to List[str]. Please adapt in generated code if this is not equal to your application."
                    # )
                    argument.type = eval(arg.annotation.slice.id)
                    argument.nargs = "+"
            if default is not None:
                if isinstance(default, ast.List):
                    argument.default = [item.value for item in default.elts]
                else:
                    argument.default = default.value

            arguments.append(argument)
        return arguments

    @staticmethod
    def _get_help_msgs(func: FunctionDef, num_args: int) -> List[str]:
        """extract help messages from docstring

        Args:
            func (FunctionDef): function to extract docstring from
            num_args (int): how many arguments are in the function

        Raises:
            ValueError: if there is a docstring missing

        Returns:
            List[str]: list of doc-strings
        """
        doc_str = ast.get_docstring(func)
        if doc_str is None:
            msg = f"No docstring for method {func.name} available"
            logging.fatal(msg)
            error_msg = f"Process was aborted because of missing doc-string in function: {func.name}"
            raise ValueError(error_msg)
        doc_str = doc_str.split("\n")
        # get argument docstring
        if num_args:
            args_index = doc_str.index("Args:") + 1
            arg_doc_strs = doc_str[args_index : args_index + num_args]  # noqa: E203
            helps = [
                ":".join(arg_doc_str.split(":")[1:]).strip(" ")
                for arg_doc_str in arg_doc_strs
            ]
        else:
            helps = []

        return helps

    def _get_command_structure(self, node: ClassDef) -> List[CommandStructure]:
        """Get the command structures defined within a class.

        Args:
            node (ClassDef): The AST node representing the class.

        Returns:
            List[CommandStructure]: A list of CommandStructure objects representing class methods as commands.
        """
        commands = []
        for func in node.body:
            # public function
            if isinstance(func, FunctionDef) and func.name[0] != "_":
                command = CommandStructure()
                command.name = func.name
                command.help = self._get_command_help(func)
                command.args.extend(self._get_arguments(func))
                commands.append(command)
        return commands

    @staticmethod
    def _get_command_help(func: FunctionDef) -> str:
        """if there is a docstring for the function extract the first line as the a help description.
        Otherwise return "---no-documentation-exists--"

        Args:
            func (FunctionDef): function definition parsed from ast

        Returns:
            str: command help
        """
        doc_str = ast.get_docstring(func)
        # if dox string is None
        if not doc_str:
            doc_str = "---no-documentation-exists--"
        else:
            doc_str = doc_str.split("\n")[0]

        return doc_str

    def parse_tree(self, tree: Module, file: str):
        """Parse the Abstract Syntax Tree (AST) of a Python module and extract structured information.

        Args:
            tree (Module): The AST of the Python module.
            file (str): The path to the Python module file.

        """
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                module = ModuleStructure()
                class_name, module_args, help = self._get_class_signature(node)
                module.name = class_name
                module.help = help
                class_commands = self._get_command_structure(node)
                module.commands.extend(class_commands)
                module.location = file
                module.args.extend(module_args)
                self.modules.modules.append(module)
