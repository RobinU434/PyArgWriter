from abc import ABC, abstractmethod
from ast import List
import json
from typing import Type


class Structure(ABC):
    def __repr__(self):
        structure = self.to_dict()
        return json.dumps(structure, indent=4)

    @classmethod
    @abstractmethod
    def from_dict(cls: "Structure", data: dict):
        raise NotImplementedError
    
    @abstractmethod
    def to_dict(self) -> dict:
        raise NotImplementedError


class ArgumentStructure(Structure):
    def __init__(self) -> None:
        self.dest: str
        self.type: Type
        self.help: str = ""
        self.default: None

    @classmethod
    def from_dict(cls: "ArgumentStructure", data):
        arg = cls()
        arg.dest = data["dest"]
        try:
            arg.type = data["type"]
        except KeyError:
            pass
        
        arg.help = data["help"]
        try:
            arg.default = data["default"]
        except KeyError:
            pass

        return arg

    def to_dict(self) -> str:
        structure = {"dest": self.dest, "help": self.help}
        
        try:
            structure["type"] = self.type.__name__
        except AttributeError:
            pass
        
        try:
            structure["default"] = self.default
        except AttributeError:
            pass
        return structure

class CommandStructure(Structure):
    def __init__(self) -> None:
        self.name: str
        self.help: str = ""
        self.args: List[ArgumentStructure] = []

    def __len__(self) -> int:
        """returns number of arguments

        Returns:
            int: number of argument for this command
        """
        return len(self.args)
    
    @classmethod
    def from_dict(cls: "CommandStructure", data: dict):
        cmd = cls()
        cmd.name = data["name"]
        cmd.help = data["help"]
        cmd.args = [ArgumentStructure.from_dict(arg) for arg in data["args"]]
        return cmd
    
    def to_dict(self) -> str:
        return {"name": self.name, "help": self.help, "args": [arg.to_dict() for arg in self.args]}
    

class ModuleStructure(Structure):
    def __init__(self) -> None:
        self.name: str
        self.help: str = ""
        self.commands: List[CommandStructure] = []
    
    def __len__(self) -> int:
        """returns number of commands

        Returns:
            int: number of commands in this module
        """
        return len(self.commands)
    
    @classmethod
    def from_dict(cls: "ModuleStructure", data: dict):
        module = cls()
        module.name = data["name"]
        module.help = data["help"]
        module.commands = [CommandStructure.from_dict(command) for command in data["commands"]]
        return module
    
    def to_dict(self) -> str:
        return {"name": self.name, "help": self.help, "commands": [ command.to_dict() for command in self.commands]}
    

class ModuleStructures(Structure):
    def __init__(self) -> None:
        super().__init__()
        self.modules: List[ModuleStructure] = []
        """List[ModuleStructure]: List of module specifications"""

    def __len__(self) -> int:
        """number of modules to create argparse structures to

        Returns:
            int: number of modules
        """
        return len(self.modules)
    @classmethod
    def from_dict(cls: "ModuleStructures", data: dict):
        modules = cls()
        modules.modules = [ModuleStructure.from_dict(module) for module in data["modules"]]
        return modules
        
    def to_dict(self) -> dict:
        return {"modules": [module.to_dict() for module in self.modules]}

