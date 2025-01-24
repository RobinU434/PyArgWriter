import ast
import inspect
import logging
from ast import ClassDef, FunctionDef, NodeVisitor
from typing import Dict, List, Tuple

from pyargwriter._core.docstring_parser import DocstringParser
from pyargwriter._core.structures import (
    ArgumentStructure,
    CommandStructure,
    DecoratorFlagStructure,
    ModuleStructure,
    ModuleStructures,
)
import pyargwriter.decorator
from pyargwriter.utils.file_system import write_json, write_yaml


class DecoratorInspector(NodeVisitor):
    def __init__(self):
        self.imports = {}  # Track imports for resolving decorator origins
        self.local_definitions = set()  # Track locally defined functions
        
        self.decorator_args = {}
        """key: decorator_name, value: arguments of decorator, default values included"""

        self.decorator_module = pyargwriter.decorator

    def visit_FunctionDef(self, node):
        self.decorator_args = {}
        self.local_definitions.add(node.name)
        for decorator in node.decorator_list:
            self.inspect_decorator(decorator)

        
    def inspect_decorator(self, decorator):
        if isinstance(decorator, ast.Name):
            pass
            # name = decorator.id
            # origin = self.resolve_origin(name)
            # print(f"  Decorator: {name}, Origin: {origin}")
        elif isinstance(decorator, ast.Attribute):
            pass
            # name = (
            #     f"{decorator.value.id}.{decorator.attr}"
            #     if isinstance(decorator.value, ast.Name)
            #     else None
            # )
            # print(f"  Decorator: {name}, Origin: External (likely)")
        elif isinstance(decorator, ast.Call) and hasattr(decorator.func, "id"):
            name = decorator.func.id

            if not self._resolve_origin(name):
                logging.info(f"decorator: {name}, did not pass import check")
                return
            
            # Extract explicitly provided args and kwargs
            args = [ast.literal_eval(arg) for arg in decorator.args]
            kwargs = {kw.arg: ast.literal_eval(kw.value) for kw in decorator.keywords}
            
            # Combine with defaults from the decorator signature
            decorator_func = getattr(self.decorator_module, name)
            final_args = self._build_arg_dict(args, kwargs, decorator_func, include_defaults=False)
            self.decorator_args[name] = final_args
        else:
            print("  Decorator: Complex or dynamic decorator, unable to resolve.")

    def update_imports(self, imports: dict[str, str]):
        self.imports = {**self.imports, **imports}
   

    def _resolve_origin(self, name: str) -> bool:
        """checks if the given decorator name comes from pyargwriter or is just defined somewhere else and has nothing to do with pyargwriter

        Args:
            name (str): name of decorator

        Returns:
            bool: True if the decorator is from pyargwriter
        """
        if name in self.local_definitions:
            # Defined in the same file
            return False
        if name in self.imports and ".".join(self.imports[name].split(".")[:-1]) == "pyargwriter.decorator":
            # Imported from pyargwriter
            return True
        else:
            # Unknown or built-in or faulty import
            return False
        
        
    def _build_arg_dict(self, args, kwargs, decorator_func, include_defaults: bool = True):
        # Get the signature of the decorator function
        sig = inspect.signature(decorator_func)

        # Build a mapping of parameter names to their defaults
        params = sig.parameters

        default_values = {}
        if include_defaults:
            default_values = {
                name: param.default
                for name, param in params.items()
                if param.default is not param.empty
            }

        # Match positional args to parameter names
        param_names = list(params.keys())
        for i, arg in enumerate(args):
            default_values[param_names[i]] = arg

        # Override with explicitly provided keyword arguments
        default_values.update(kwargs)

        return default_values
    
    def get_decorator_flag_structs(self) -> List[DecoratorFlagStructure]:
        res = []
        for name, args in self.decorator_args.items():
            flag_struct = DecoratorFlagStructure()
            flag_struct.name = name
            flag_struct.values = args
            res.append(flag_struct)
        return res


class ClassInspector(NodeVisitor):
    """inspect class internals like the functions, ..."""

    def __init__(self, docstring_format: str = "google"):
        super().__init__()

        self._func_signatures: Dict[str, Tuple[List[ArgumentStructure], str, List[DecoratorFlagStructure]]] = {}
        """dict[str, Tuple[List[ArgumentStructure], str]: key: func_name, value:"""

        self.decorator_inspector = DecoratorInspector()
        self.docstring_parser = DocstringParser.build_parser(docstring_format)

    def visit_FunctionDef(self, node: FunctionDef):
        if node.name == "__init__":
            # 1. do init stuff
            arguments = self._get_arguments(node)

            self._func_signatures[node.name] = (arguments, None, [])

        elif node.name[0] != "_":
            # 2. only use functions marked as public functions
            self.decorator_inspector.visit_FunctionDef(node)
            decorator_flag_structs = self.decorator_inspector.get_decorator_flag_structs()
            arguments = self._get_arguments(node, exceptions=self._get_argument_exceptions(decorator_flag_structs))
            help_message = self.docstring_parser.get_help_msg(node)
            # help_message, _ = self._get_help_msgs(node)
            
            self._func_signatures[node.name] = (arguments, help_message, decorator_flag_structs)

        # ignore other functions

    def _get_arguments(self, func: FunctionDef, exceptions: List[str] = []) -> List[ArgumentStructure]:
        """Get the arguments of a function.

        Args:
            func (FunctionDef): The AST node representing the function.
            exceptions (str): Arguments to be skipped

        Returns:
            List[ArgumentStructure]: A list of ArgumentStructure objects representing function arguments.
        """
        num_args = len(func.args.args)
        name_decorator = list(filter(lambda x: isinstance(x, ast.Name), func.decorator_list))
        if "staticmethod" not in [decorator.id for decorator in name_decorator]:
            num_args -= 1
        _, helps = self._get_help_msgs(func)

        # add defaults
        defaults = [None] * num_args
        if len(func.args.defaults):
            defaults[-len(func.args.defaults) :] = func.args.defaults  # noqa: E203

        arguments = []
        for arg, help_message, default in zip(
            func.args.args[-num_args:], helps, defaults
        ):  
            if arg.arg in exceptions:
                continue
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
    def _get_argument_exceptions(decorator_structs: List[DecoratorFlagStructure]) -> List[str]:
        res = []
        for decorator_struct in decorator_structs:
            name = decorator_struct.name
            if name == pyargwriter.decorator.add_hydra.__name__:
                sig = inspect.signature(pyargwriter.decorator.add_hydra)
                # Build a mapping of parameter names to their defaults
                params = sig.parameters
                default_values = {
                    name: param.default
                    for name, param in params.items()
                    if param.default is not param.empty
                }
                default_values.update(decorator_struct.values)
                res.append(default_values["config_var_name"])
        return res


    def _get_help_msgs(self, func: FunctionDef) -> Tuple[str, List[str]]:
        """extract help messages from docstring

        Args:
            func (FunctionDef): function to extract docstring from

        Raises:
            ValueError: if there is a docstring missing

        Returns:
            Tuple[str, List[str]]: first line in docstring, list of doc-strings for each argument
        """
        first_line = self.docstring_parser.get_help_msg(func)
        helps = self.docstring_parser.get_arg_help_msg(func).values()
        helps = list(helps)
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
        for name, (args, help_msg, decorator_flag) in working_copy.items():
            command = CommandStructure()
            command.name = name
            command.args.extend(args)
            command.decorator_flags.extend(decorator_flag)
            command.help = help_msg
            commands.append(command)
        return commands


class ModuleInspector(NodeVisitor):
    def __init__(self, docstring_format: str = "google"):
        super().__init__()

        self.func_inspector = ClassInspector(docstring_format)
        self.docstring_parser = DocstringParser.build_parser(docstring_format)
        self._modules = ModuleStructures()
        self.imports = {}

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
    
    def visit_Import(self, node):
        for alias in node.names:
            self.imports[alias.asname or alias.name] = alias.name

    def visit_ImportFrom(self, node):
        module = node.module
        for alias in node.names:
            full_name = f"{module}.{alias.name}" if module else alias.name
            self.imports[alias.asname or alias.name] = full_name

    def visit_ClassDef(self, node: ClassDef):
        module_structure = ModuleStructure()
        module_structure.name = node.name

        self.func_inspector.decorator_inspector.update_imports(self.imports)
        self.func_inspector.visit(node)
        init_args = self.func_inspector.init_args
        module_structure.args.extend(init_args)
        module_structure.help = self._get_class_help_msg(node)

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
        help_message = self.docstring_parser.get_help_msg(node)
        return help_message

    @property
    def modules(self) -> ModuleStructures:
        return self._modules
