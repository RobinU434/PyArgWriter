from ast import ClassDef, FunctionDef, NodeVisitor
import ast
from typing import Tuple, Dict, List
from pyargwriter.utils.file_system import write_json, write_yaml
from pyargwriter._core.structures import (
    ArgumentStructure,
    CommandStructure,
    ModuleStructure,
    ModuleStructures,
)
import logging

class ClassInspector(NodeVisitor):
    """inspect class internals like the functions, ...
    """
    def __init__(self):
        super().__init__()
        
        self._func_signatures: Dict[str, Tuple[List[ArgumentStructure], str]] = {}
        """dict[str, Tuple[List[ArgumentStructure], str]: key: func_name, value:"""
    
    def visit_FunctionDef(self, node: FunctionDef):
        if node.name == "__init__":
            # 1. do init stuff
            arguments = self._get_arguments(node)
            
            self._func_signatures[node.name] = (arguments, None)

            
        elif node.name[0] != "_":
            # 2. only use functions marked as public functions
            arguments = self._get_arguments(node)
            help_message, _ = self._get_help_msgs(node, 0)

            self._func_signatures[node.name] = (arguments, help_message)
        # ignore other functions
    
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
        _, helps = self._get_help_msgs(func, num_args)

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
    def _get_help_msgs(func: FunctionDef, num_args: int = 0) -> Tuple[str, List[str]]:
        """extract help messages from docstring

        Args:
            func (FunctionDef): function to extract docstring from
            num_args (int): how many arguments are in the function

        Raises:
            ValueError: if there is a docstring missing

        Returns:
            Tuple[str, List[str]]: first line in docstring, list of doc-strings for each argument
        """
        doc_str = ast.get_docstring(func)
        if doc_str is None:
            msg = f"No docstring for method {func.name} available"
            logging.fatal(msg)
            error_msg = f"Process was aborted because of missing doc-string in function: {func.name}"
            raise ValueError(error_msg)
        doc_str = doc_str.split("\n")
        first_line = doc_str[0] if len(doc_str[0]) > 0 else doc_str[1]
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

        return first_line, helps
    
    @property
    def init_args(self) -> List[ArgumentStructure]:
        if "__init__" not in self._func_signatures:
            return []
        return self._func_signatures["__init__"][0]
    
    @property
    def public_def(self) -> List[CommandStructure]:
        working_copy = self._func_signatures.copy()
        if "__init__" in self._func_signatures:
            working_copy.pop("__init__")
        
        commands = []
        for name, (args, help_msg) in working_copy.items():
            command = CommandStructure()
            command.name = name
            command.args.extend(args)
            command.help_msg = help_msg
            commands.append(command)
        return commands
    
class ModuleInspector(NodeVisitor):
    def __init__(self):
        super().__init__()

        self.func_inspector = ClassInspector()
        self._modules = ModuleStructures()

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

    def visit_ClassDef(self, node: ClassDef):
        module_structure = ModuleStructure()
        module_structure.name = node.name
        
        self.func_inspector.visit(node)
        
        init_args = self.func_inspector.init_args
        module_structure.args.extend(init_args)
        module_structure.help_msg = self._get_class_help_msg(node)

        module_structure.commands.extend(self.func_inspector.public_def)
        self._modules.modules.append(module_structure)

    def visit(self, node, location: str = None):
        super().visit(node)

        for ms in self._modules.modules:
            if hasattr(ms, "location") or location is None:
                continue
            ms.location = location

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

    def _get_class_help_msg(self, node: ClassDef) -> str:
        """Get the signature (name and arguments) of a class.

        Args:
            node (ClassDef): The AST node representing the class.

        Returns:
            str: a short explanation what the class represents.
        """
        docstring = ast.get_docstring(node)
        if docstring is None:
            logging.info("No docstring in class declaration found.")
            help_message = ""
        else:
            help_message = docstring.split("\n")[0]
        return help_message

    @property
    def modules(self) -> ModuleStructures:
        return self._modules
    
    
        
"""
inspector = ModuleInspector()

filename = "examples/shopping.py"
with open(filename, "r") as file:
    tree = ast.parse(file.read())
inspector.visit(tree, filename)
filename = "examples/car.py"
with open(filename, "r") as file:
    tree = ast.parse(file.read())
inspector.visit(tree, filename)

len(inspector.modules.modules)
print(inspector.modules)"""