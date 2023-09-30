from abc import ABC
from ast import AST, ClassDef, Expr, FunctionDef, Module
import ast
import json
import logging
from typing import Any, List, Type

from pyargwriter.utils.file_system import write_json, write_yaml
from pyargwriter.utils.structures import ArgumentStructure, CommandStructure, ModuleStructure, ModuleStructures

    
class CodeParser:
    def __init__(self) -> None:
        self.modules = ModuleStructures()

    def __repr__(self) -> str:
        result = "["
        for module in self.modules:
            result += repr(module)
            result += ",\n"
        result = result.rstrip(",\n")
        result += "]"
        return result
    
    @property
    def module_serialized(self):
        result = []
        for module in self.modules:
            result.append(module.to_dict())
        return result

    def write(self, path: str):
        file_type = path.split(".")[-1]
        match file_type:
            case "yaml":
                write_func = write_yaml
            case "yml":
                write_func = write_yaml
            case "json":
                write_func = write_json
            case _:
                logging.warning(f"Not implemented write method for file type {file_type}")
        write_func(self.modules.to_dict(), path)
                
    @staticmethod
    def _get_class_signature(node):
        class_name = node.name
        args = []
        for item in node.body:
            if isinstance(item, ast.FunctionDef) and item.name == "__init__":
                for arg in item.args.args[1:]:  # Exclude 'self' argument
                    if isinstance(arg, ast.arg):
                        args.append(arg.arg)
        return class_name, args
    
    @staticmethod
    def _get_arguments(func: FunctionDef) -> List[ArgumentStructure]:
        num_args = len(func.args.args)
        if "staticmethod" not in [decorator.id for decorator in func.decorator_list]:
            num_args -= 1
        doc_str = ast.get_docstring(func).split("\n")
        #get argument docstring
        if num_args:
            args_index = doc_str.index("Args:") + 1
            arg_doc_strs = doc_str[args_index:args_index+num_args]
            helps = [":".join(arg_doc_str.split(":")[1:]).strip(" ") for arg_doc_str in arg_doc_strs]
        else:
            helps = []


        # add defaults
        defaults = [None] * num_args
        if len(func.args.defaults):
            defaults[-len(func.args.defaults):] = func.args.defaults
        
        arguments = []
        for arg, help, default in zip(func.args.args[-num_args:], helps, defaults):
            argument = ArgumentStructure()
            argument.dest = arg.arg
            argument.help = help
            
            if arg.annotation:
                argument.type = eval(arg.annotation.id)
            
            if default is not None:
                argument.default = default.value
            
            arguments.append(argument)
        return arguments
        
    def _get_command_structure(self, node: ClassDef) -> List[CommandStructure]:
        commands = []
        for func in node.body:
            # public function
            if isinstance(func, FunctionDef) and func.name[0] != "_":
                command = CommandStructure()
                command.name = func.name
                doc_str = ast.get_docstring(func)
                command.help = doc_str.split("\n")[0]
                command.args.extend(self._get_arguments(func))
                commands.append(command)
        return commands
    
    def parse_tree(self, tree: Module):
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                module = ModuleStructure()
                class_name, args = self._get_class_signature(node)
                module.name = class_name
                class_commands = self._get_command_structure(node)
                module.commands.extend(class_commands)
                self.modules.modules.append(module)