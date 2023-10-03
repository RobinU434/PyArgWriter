from __future__ import annotations
from abc import ABC, abstractmethod
from ast import List
import json
from typing import Dict, Type


class Structure(ABC):
    def __repr__(self):
        structure = self.to_dict()
        return json.dumps(structure, indent=4)

    @classmethod
    @abstractmethod
    def from_dict(cls: Structure, data: dict):
        raise NotImplementedError

    @abstractmethod
    def to_dict(self) -> dict:
        raise NotImplementedError


class ArgumentStructure(Structure):
    def __init__(self) -> None:
        self.name_or_flags: str
        self.dest: str
        self.type: Type
        self.help: str = ""
        self.default: None

    @classmethod
    def from_dict(cls: ArgumentStructure, data: Dict[str, str]):
        arg = cls()
        arg.dest = data["dest"]
        arg.name_or_flags = data["name_or_flags"]
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
        structure = {
            "name_or_flags": self.name_or_flags,
            "dest": self.dest,
            "help": self.help,
        }

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
    def from_dict(cls: CommandStructure, data: dict):
        cmd = cls()
        cmd.name = data["name"]
        cmd.help = data["help"]
        cmd.args = [ArgumentStructure.from_dict(arg) for arg in data["args"]]
        return cmd

    def to_dict(self) -> str:
        return {
            "name": self.name,
            "help": self.help,
            "args": [arg.to_dict() for arg in self.args],
        }


class ModuleStructure(Structure):
    def __init__(self) -> None:
        self.name: str
        self.help: str = ""
        self.commands: List[CommandStructure] = []

        self.location: str
        """str: where the module can be found. Important for imports in main file"""
        self.args: List[ArgumentStructure] = []
        """List[ArgumentStructure]: List of arguments needed for create module instance"""

    def __len__(self) -> int:
        """returns number of commands

        Returns:
            int: number of commands in this module
        """
        return len(self.commands)

    @classmethod
    def from_dict(cls: ModuleStructure, data: Dict[str, str]):
        module: ModuleStructure = cls()
        module.name = data["name"]
        module.help = data["help"]
        module.commands = [
            CommandStructure.from_dict(command) for command in data["commands"]
        ]
        module.location = data["location"]
        module.args = [ArgumentStructure.from_dict(arg) for arg in data["args"]]

        return module

    def to_dict(self) -> str:
        return {
            "name": self.name,
            "help": self.help,
            "commands": [command.to_dict() for command in self.commands],
            "location": self.location,
            "args": [arg.to_dict() for arg in self.args],
        }

    def add_args(self, args: List[ArgumentStructure]) -> None:
        """adds given arguments to all commands

        Args:
            args (List[ArgumentStructure]): list of arguments
        """
        for command in self.commands:
            command: CommandStructure
            command.args.extend(args)


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
    def from_dict(cls: ModuleStructures, data: Dict[str, str]):
        modules: ModuleStructures = cls()
        modules.modules = [
            ModuleStructure.from_dict(module) for module in data["modules"]
        ]
        return modules

    def to_dict(self) -> dict:
        return {"modules": [module.to_dict() for module in self.modules]}

    @property
    def locations(self):
        """returns dict of module name and corresponding location"""
        locations = {}
        for module in self.modules:
            module: ModuleStructure
            locations[module.name] = module.location
        return locations
