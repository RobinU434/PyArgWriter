from __future__ import annotations
from abc import ABC, abstractmethod
from ast import List
import json
import logging
from typing import Dict, Type


class Structure(ABC):
    """Abstract base class for defining structured objects.

    This class defines methods for converting structured objects to and from dictionaries,
    as well as providing a JSON representation of the object.

    Attributes:
        None

    Methods:
        from_dict(cls, data: dict) -> Structure:
            Abstract method for creating an instance of the class from a dictionary.

        to_dict(self) -> dict:
            Abstract method for converting the object to a dictionary representation.

    """

    def __repr__(self):
        """Return a JSON representation of the structured object."""
        structure = self.to_dict()
        return json.dumps(structure, indent=4)

    @classmethod
    @abstractmethod
    def from_dict(cls: Structure, data: dict):
        """Create an instance of the class from a dictionary.

        Args:
            cls (Type[Structure]): The class itself.
            data (dict): The dictionary containing data to create the instance from.

        Raises:
            NotImplementedError: This method should be implemented in subclasses.

        Returns:
            Structure: An instance of the class created from the dictionary.
        """
        raise NotImplementedError

    @abstractmethod
    def to_dict(self) -> dict:
        """Convert the object to a dictionary representation.

        Raises:
            NotImplementedError: This method should be implemented in subclasses.

        Returns:
            dict: A dictionary representation of the object.
        """
        raise NotImplementedError


class ArgumentStructure(Structure):
    def __init__(self) -> None:
        """Class representing an argument structure.

        This class defines the structure for command-line arguments.

        Attributes:
            name_or_flags (str): The name or flags for the argument.
            dest (str): The destination attribute for the argument.
            type (Type): The data type of the argument.
            help (str): The help text for the argument.
            default (None): The default value for the argument (default is None).

        Methods:
            from_dict(cls, data: Dict[str, str]) -> ArgumentStructure:
                Create an instance of the class from a dictionary.

            to_dict(self) -> dict:
                Convert the argument structure to a dictionary representation.

        """
        self.name_or_flags: str
        self.dest: str
        self.type: Type
        self.nargs: str
        self.help: str = ""
        self.default: None

    @classmethod
    def from_dict(cls: ArgumentStructure, data: Dict[str, str]) -> ArgumentStructure:
        """Create an instance of the ArgumentStructure class from a dictionary.

        Args:
            cls (Type[ArgumentStructure]): The class itself.
            data (Dict[str, str]): The dictionary containing data to create the instance from.

        Returns:
            ArgumentStructure: An instance of the ArgumentStructure class created from the dictionary.
        """
        arg = cls()
        for key, value in data.items():
            setattr(arg, key, value)

        return arg

    def to_dict(self) -> Dict[str, str]:
        """Convert the argument structure to a dictionary representation.

        Returns:
            dict: A dictionary representation of the argument structure.
        """
        structure = {}
        for name, value in vars(self).items():
            if isinstance(value, Type):
                value = value.__name__
            structure[name] = value

        # check if the minimal number of args is in the dict:
        required_keys = set(["name_or_flags", "dest", "help"])
        keys = set(structure.keys())
        if required_keys.intersection(keys) != required_keys:
            logging.warning("There are keys in the generated structure missing")

        return structure


class CommandStructure(Structure):
    """Class representing a command structure.

    This class defines the structure for commands.

    Attributes:
        name (str): The name of the command.
        help (str): The help text for the command.
        args (List[ArgumentStructure]): A list of ArgumentStructure objects representing command arguments.

    Methods:
        from_dict(cls, data: dict) -> CommandStructure:
            Create an instance of the class from a dictionary.

        to_dict(self) -> dict:
            Convert the command structure to a dictionary representation.

    """

    def __init__(self) -> None:
        self.name: str
        self.help: str = ""
        self.args: List[ArgumentStructure] = []

    def __len__(self) -> int:
        """Return the number of arguments for this command.

        Returns:
            int: The number of arguments for this command.
        """
        return len(self.args)

    @classmethod
    def from_dict(cls: CommandStructure, data: dict) -> CommandStructure:
        """Create an instance of the CommandStructure class from a dictionary.

        Args:
            cls (Type[CommandStructure]): The class itself.
            data (dict): The dictionary containing data to create the instance from.

        Returns:
            CommandStructure: An instance of the CommandStructure class created from the dictionary.
        """
        cmd = cls()
        cmd.name = data["name"]
        cmd.help = data["help"]
        cmd.args = [ArgumentStructure.from_dict(arg) for arg in data["args"]]
        return cmd

    def to_dict(self) -> Dict[str, str]:
        """Convert the command structure to a dictionary representation.

        Returns:
            dict: A dictionary representation of the command structure.
        """
        return {
            "name": self.name,
            "help": self.help,
            "args": [arg.to_dict() for arg in self.args],
        }


class ModuleStructure(Structure):
    """Class representing a module structure.

    This class defines the structure for modules.

    Attributes:
        name (str): The name of the module.
        help (str): The help text for the module.
        commands (List[CommandStructure]): A list of CommandStructure objects representing module commands.
        location (str): The location where the module can be found (important for imports in the main file).
        args (List[ArgumentStructure]): A list of ArgumentStructure objects representing arguments needed to create a module instance.

    Methods:
        from_dict(cls, data: Dict[str, str]) -> ModuleStructure:
            Create an instance of the class from a dictionary.

        to_dict(self) -> dict:
            Convert the module structure to a dictionary representation.

        add_args(self, args: List[ArgumentStructure]) -> None:
            Add given arguments to all commands in the module.

    """

    def __init__(self) -> None:
        self.name: str
        self.help: str = ""
        self.commands: List[CommandStructure] = []

        self.location: str
        """str: where the module can be found. Important for imports in main file"""
        self.args: List[ArgumentStructure] = []
        """List[ArgumentStructure]: List of arguments needed for create module instance"""

    def __len__(self) -> int:
        """Return the number of commands in this module.

        Returns:
            int: The number of commands in this module.
        """
        return len(self.commands)

    @classmethod
    def from_dict(cls: ModuleStructure, data: Dict[str, str]) -> ModuleStructure:
        """Create an instance of the ModuleStructure class from a dictionary.

        Args:
            cls (Type[ModuleStructure]): The class itself.
            data (Dict[str, str]): The dictionary containing data to create the instance from.

        Returns:
            ModuleStructure: An instance of the ModuleStructure class created from the dictionary.
        """
        module: ModuleStructure = cls()
        module.name = data["name"]
        module.help = data["help"]
        module.commands = [
            CommandStructure.from_dict(command) for command in data["commands"]
        ]
        module.location = data["location"]
        module.args = [ArgumentStructure.from_dict(arg) for arg in data["args"]]

        return module

    def to_dict(self) -> Dict[str, str]:
        """Convert the module structure to a dictionary representation.

        Returns:
            dict: A dictionary representation of the module structure.
        """
        return {
            "name": self.name,
            "help": self.help,
            "commands": [command.to_dict() for command in self.commands],
            "location": self.location,
            "args": [arg.to_dict() for arg in self.args],
        }

    def add_args(self, args: List[ArgumentStructure]) -> None:
        """Add given arguments to all commands in the module.

        Args:
            args (List[ArgumentStructure]): A list of arguments to add to the module's commands.
        """
        for command in self.commands:
            command: CommandStructure
            command.args.extend(args)


class ModuleStructures(Structure):
    """Class representing a collection of module structures.

    This class defines a collection of ModuleStructure objects.

    Attributes:
        modules (List[ModuleStructure]): A list of ModuleStructure objects representing module specifications.

    Methods:
        from_dict(cls, data: Dict[str, str]) -> ModuleStructures:
            Create an instance of the class from a dictionary.

        to_dict(self) -> dict:
            Convert the collection of module structures to a dictionary representation.

    Properties:
        locations:
            Returns a dictionary of module names and their corresponding locations.

    """

    def __init__(self) -> None:
        super().__init__()
        self.modules: List[ModuleStructure] = []
        """List[ModuleStructure]: List of module specifications"""

    def __len__(self) -> int:
        """Return the number of modules in the collection.

        Returns:
            int: The number of modules in the collection.
        """
        return len(self.modules)

    @classmethod
    def from_dict(cls: ModuleStructures, data: Dict[str, str]):
        """Create an instance of the ModuleStructures class from a dictionary.

        Args:
            cls (Type[ModuleStructures]): The class itself.
            data (Dict[str, str]): The dictionary containing data to create the instance from.

        Returns:
            ModuleStructures: An instance of the ModuleStructures class created from the dictionary.
        """
        modules: ModuleStructures = cls()
        modules.modules = [
            ModuleStructure.from_dict(module) for module in data["modules"]
        ]
        return modules

    def to_dict(self) -> Dict[str, str]:
        """Convert the collection of module structures to a dictionary representation.

        Returns:
            dict: A dictionary representation of the collection of module structures.
        """
        return {"modules": [module.to_dict() for module in self.modules]}

    @property
    def locations(self) -> Dict[str, str]:
        """Return a dictionary of module names and their corresponding locations.

        Returns:
            dict: A dictionary mapping module names to their corresponding locations.
        """
        locations = {}
        for module in self.modules:
            module: ModuleStructure
            locations[module.name] = module.location
        return locations

    @property
    def names(self) -> List[str]:
        """Return a list of module names.

        Returns:
            List[str]: A list containing names of all modules.
        """
        module_names = []
        for module in self.modules:
            module: ModuleStructure
            module_names.append(module.name)

        return module_names
