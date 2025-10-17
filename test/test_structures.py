"""Test cases for pyargwriter._core.structures module.

This module contains comprehensive tests for the structure classes:
ArgumentStructure, CommandStructure, ModuleStructure, ModuleStructures, and DecoratorFlagStructure.
"""

import pytest
import json
from pyargwriter._core.structures import (
    ArgumentStructure,
    CommandStructure,
    ModuleStructure,
    ModuleStructures,
    DecoratorFlagStructure,
)


class TestArgumentStructure:
    """Test cases for ArgumentStructure class."""

    def test_argument_structure_creation(self):
        """Test creating an ArgumentStructure."""
        arg = ArgumentStructure()
        arg.name_or_flags = "input_file"
        arg.dest = "input_file"
        arg.type = str
        arg.help = "Path to input file"
        
        assert arg.name_or_flags == "input_file"
        assert arg.dest == "input_file"
        assert arg.type == str
        assert arg.help == "Path to input file"

    def test_argument_structure_to_dict(self):
        """Test converting ArgumentStructure to dictionary."""
        arg = ArgumentStructure()
        arg.name_or_flags = "count"
        arg.dest = "count"
        arg.type = int
        arg.help = "Number of items"
        arg.default = 10
        
        result = arg.to_dict()
        
        assert result["name_or_flags"] == "count"
        assert result["dest"] == "count"
        assert result["type"] == "int"
        assert result["help"] == "Number of items"
        assert result["default"] == 10

    def test_argument_structure_from_dict(self):
        """Test creating ArgumentStructure from dictionary."""
        data = {
            "name_or_flags": "output",
            "dest": "output",
            "type": "str",
            "help": "Output path",
            "default": "./output"
        }
        
        arg = ArgumentStructure.from_dict(data)
        
        assert arg.name_or_flags == "output"
        assert arg.dest == "output"
        assert arg.type == "str"
        assert arg.help == "Output path"
        assert arg.default == "./output"

    def test_argument_structure_repr(self):
        """Test JSON representation of ArgumentStructure."""
        arg = ArgumentStructure()
        arg.name_or_flags = "verbose"
        arg.dest = "verbose"
        arg.type = bool
        arg.help = "Enable verbose mode"
        
        repr_str = repr(arg)
        parsed = json.loads(repr_str)
        
        assert parsed["name_or_flags"] == "verbose"
        assert parsed["dest"] == "verbose"
        assert parsed["help"] == "Enable verbose mode"

    def test_argument_structure_with_nargs(self):
        """Test ArgumentStructure with nargs for list arguments."""
        arg = ArgumentStructure()
        arg.name_or_flags = "files"
        arg.dest = "files"
        arg.type = str
        arg.nargs = "+"
        arg.help = "List of files"
        
        result = arg.to_dict()
        assert result["nargs"] == "+"

    def test_argument_structure_with_list_default(self):
        """Test ArgumentStructure with list as default value."""
        arg = ArgumentStructure()
        arg.name_or_flags = "items"
        arg.dest = "items"
        arg.type = int
        arg.default = [1, 2, 3]
        arg.help = "List of items"
        
        result = arg.to_dict()
        assert result["default"] == [1, 2, 3]


class TestDecoratorFlagStructure:
    """Test cases for DecoratorFlagStructure class."""

    def test_decorator_flag_creation(self):
        """Test creating a DecoratorFlagStructure."""
        flag = DecoratorFlagStructure()
        flag.name = "add_hydra"
        flag.values = {"config_var_name": "cfg", "config_path": "conf"}
        
        assert flag.name == "add_hydra"
        assert flag.values["config_var_name"] == "cfg"
        assert flag.values["config_path"] == "conf"

    def test_decorator_flag_to_dict(self):
        """Test converting DecoratorFlagStructure to dictionary."""
        flag = DecoratorFlagStructure()
        flag.name = "add_hydra"
        flag.values = {"config_name": "config.yaml"}
        
        result = flag.to_dict()
        
        assert result["name"] == "add_hydra"
        assert result["values"]["config_name"] == "config.yaml"

    def test_decorator_flag_from_dict(self):
        """Test creating DecoratorFlagStructure from dictionary."""
        data = {
            "name": "add_custom_decorator",
            "values": {"param1": "value1", "param2": 42}
        }
        
        flag = DecoratorFlagStructure.from_dict(data)
        
        assert flag.name == "add_custom_decorator"
        assert flag.values["param1"] == "value1"
        assert flag.values["param2"] == 42


class TestCommandStructure:
    """Test cases for CommandStructure class."""

    def test_command_structure_creation(self):
        """Test creating a CommandStructure."""
        cmd = CommandStructure()
        cmd.name = "train"
        cmd.help = "Train the model"
        
        arg1 = ArgumentStructure()
        arg1.name_or_flags = "epochs"
        arg1.dest = "epochs"
        arg1.type = int
        arg1.help = "Number of epochs"
        
        cmd.args.append(arg1)
        
        assert cmd.name == "train"
        assert cmd.help == "Train the model"
        assert len(cmd.args) == 1
        assert cmd.args[0].name_or_flags == "epochs"

    def test_command_structure_length(self):
        """Test __len__ method of CommandStructure."""
        cmd = CommandStructure()
        assert len(cmd) == 0
        
        cmd.args.append(ArgumentStructure())
        assert len(cmd) == 1
        
        cmd.args.append(ArgumentStructure())
        assert len(cmd) == 2

    def test_command_structure_to_dict(self):
        """Test converting CommandStructure to dictionary."""
        cmd = CommandStructure()
        cmd.name = "evaluate"
        cmd.help = "Evaluate model"
        
        arg = ArgumentStructure()
        arg.name_or_flags = "metric"
        arg.dest = "metric"
        arg.type = str
        arg.help = "Evaluation metric"
        cmd.args.append(arg)
        
        flag = DecoratorFlagStructure()
        flag.name = "add_logging"
        flag.values = {"level": "INFO"}
        cmd.decorator_flags.append(flag)
        
        result = cmd.to_dict()
        
        assert result["name"] == "evaluate"
        assert result["help"] == "Evaluate model"
        assert len(result["args"]) == 1
        assert result["args"][0]["name_or_flags"] == "metric"
        assert len(result["decorator_flags"]) == 1
        assert result["decorator_flags"][0]["name"] == "add_logging"

    def test_command_structure_from_dict(self):
        """Test creating CommandStructure from dictionary."""
        data = {
            "name": "predict",
            "help": "Make predictions",
            "args": [
                {
                    "name_or_flags": "model_path",
                    "dest": "model_path",
                    "type": "str",
                    "help": "Path to model"
                }
            ],
            "decorator_flags": [
                {
                    "name": "add_timing",
                    "values": {"enabled": True}
                }
            ]
        }
        
        cmd = CommandStructure.from_dict(data)
        
        assert cmd.name == "predict"
        assert cmd.help == "Make predictions"
        assert len(cmd.args) == 1
        assert cmd.args[0].name_or_flags == "model_path"
        assert len(cmd.decorator_flags) == 1
        assert cmd.decorator_flags[0].name == "add_timing"

    def test_command_structure_empty(self):
        """Test CommandStructure with no arguments."""
        cmd = CommandStructure()
        cmd.name = "status"
        cmd.help = "Check status"
        
        result = cmd.to_dict()
        assert result["name"] == "status"
        assert result["args"] == []
        assert result["decorator_flags"] == []


class TestModuleStructure:
    """Test cases for ModuleStructure class."""

    def test_module_structure_creation(self):
        """Test creating a ModuleStructure."""
        module = ModuleStructure()
        module.name = "Calculator"
        module.help = "Calculator module"
        module.location = "src/calculator.py"
        
        assert module.name == "Calculator"
        assert module.help == "Calculator module"
        assert module.location == "src/calculator.py"

    def test_module_structure_length(self):
        """Test __len__ method of ModuleStructure."""
        module = ModuleStructure()
        assert len(module) == 0
        
        cmd1 = CommandStructure()
        cmd1.name = "add"
        module.commands.append(cmd1)
        assert len(module) == 1
        
        cmd2 = CommandStructure()
        cmd2.name = "subtract"
        module.commands.append(cmd2)
        assert len(module) == 2

    def test_module_structure_add_args(self):
        """Test add_args method to add arguments to all commands."""
        module = ModuleStructure()
        
        cmd1 = CommandStructure()
        cmd1.name = "process"
        module.commands.append(cmd1)
        
        cmd2 = CommandStructure()
        cmd2.name = "analyze"
        module.commands.append(cmd2)
        
        # Add common arguments to all commands
        common_arg = ArgumentStructure()
        common_arg.name_or_flags = "verbose"
        common_arg.dest = "verbose"
        common_arg.type = bool
        common_arg.help = "Verbose output"
        
        module.add_args([common_arg])
        
        assert len(module.commands[0].args) == 1
        assert len(module.commands[1].args) == 1
        assert module.commands[0].args[0].name_or_flags == "verbose"
        assert module.commands[1].args[0].name_or_flags == "verbose"

    def test_module_structure_to_dict(self):
        """Test converting ModuleStructure to dictionary."""
        module = ModuleStructure()
        module.name = "DataProcessor"
        module.help = "Process data"
        module.location = "src/processor.py"
        
        arg = ArgumentStructure()
        arg.name_or_flags = "input_dir"
        arg.dest = "input_dir"
        arg.type = str
        arg.help = "Input directory"
        module.args.append(arg)
        
        cmd = CommandStructure()
        cmd.name = "run"
        cmd.help = "Run processing"
        module.commands.append(cmd)
        
        result = module.to_dict()
        
        assert result["name"] == "DataProcessor"
        assert result["help"] == "Process data"
        assert result["location"] == "src/processor.py"
        assert len(result["args"]) == 1
        assert len(result["commands"]) == 1

    def test_module_structure_from_dict(self):
        """Test creating ModuleStructure from dictionary."""
        data = {
            "name": "FileManager",
            "help": "Manage files",
            "location": "src/file_manager.py",
            "args": [
                {
                    "name_or_flags": "base_path",
                    "dest": "base_path",
                    "type": "str",
                    "help": "Base path"
                }
            ],
            "commands": [
                {
                    "name": "list",
                    "help": "List files",
                    "args": [],
                    "decorator_flags": []
                }
            ]
        }
        
        module = ModuleStructure.from_dict(data)
        
        assert module.name == "FileManager"
        assert module.help == "Manage files"
        assert module.location == "src/file_manager.py"
        assert len(module.args) == 1
        assert len(module.commands) == 1


class TestModuleStructures:
    """Test cases for ModuleStructures class."""

    def test_module_structures_creation(self):
        """Test creating a ModuleStructures collection."""
        modules = ModuleStructures()
        assert len(modules) == 0
        assert len(modules.modules) == 0

    def test_module_structures_length(self):
        """Test __len__ method of ModuleStructures."""
        modules = ModuleStructures()
        assert len(modules) == 0
        
        module1 = ModuleStructure()
        module1.name = "Module1"
        modules.modules.append(module1)
        assert len(modules) == 1
        
        module2 = ModuleStructure()
        module2.name = "Module2"
        modules.modules.append(module2)
        assert len(modules) == 2

    def test_module_structures_locations_property(self):
        """Test locations property that returns module name to location mapping."""
        modules = ModuleStructures()
        
        module1 = ModuleStructure()
        module1.name = "Parser"
        module1.location = "src/parser.py"
        modules.modules.append(module1)
        
        module2 = ModuleStructure()
        module2.name = "Analyzer"
        module2.location = "src/analyzer.py"
        modules.modules.append(module2)
        
        locations = modules.locations
        
        assert len(locations) == 2
        assert locations["Parser"] == "src/parser.py"
        assert locations["Analyzer"] == "src/analyzer.py"

    def test_module_structures_names_property(self):
        """Test names property that returns list of module names."""
        modules = ModuleStructures()
        
        module1 = ModuleStructure()
        module1.name = "ModuleA"
        modules.modules.append(module1)
        
        module2 = ModuleStructure()
        module2.name = "ModuleB"
        modules.modules.append(module2)
        
        names = modules.names
        
        assert len(names) == 2
        assert "ModuleA" in names
        assert "ModuleB" in names

    def test_module_structures_to_dict(self):
        """Test converting ModuleStructures to dictionary."""
        modules = ModuleStructures()
        
        module = ModuleStructure()
        module.name = "TestModule"
        module.help = "Test module"
        module.location = "test.py"
        module.args = []
        module.commands = []
        modules.modules.append(module)
        
        result = modules.to_dict()
        
        assert "modules" in result
        assert len(result["modules"]) == 1
        assert result["modules"][0]["name"] == "TestModule"

    def test_module_structures_from_dict(self):
        """Test creating ModuleStructures from dictionary."""
        data = {
            "modules": [
                {
                    "name": "Module1",
                    "help": "First module",
                    "location": "module1.py",
                    "args": [],
                    "commands": []
                },
                {
                    "name": "Module2",
                    "help": "Second module",
                    "location": "module2.py",
                    "args": [],
                    "commands": []
                }
            ]
        }
        
        modules = ModuleStructures.from_dict(data)
        
        assert len(modules) == 2
        assert modules.modules[0].name == "Module1"
        assert modules.modules[1].name == "Module2"

    def test_module_structures_repr(self):
        """Test JSON representation of ModuleStructures."""
        modules = ModuleStructures()
        
        module = ModuleStructure()
        module.name = "ReprTest"
        module.help = "Repr test"
        module.location = "test.py"
        module.args = []
        module.commands = []
        modules.modules.append(module)
        
        repr_str = repr(modules)
        parsed = json.loads(repr_str)
        
        assert "modules" in parsed
        assert len(parsed["modules"]) == 1


class TestStructuresIntegration:
    """Integration tests for structure classes working together."""

    def test_complete_module_structure(self):
        """Test creating a complete module structure with all components."""
        # Create module
        module = ModuleStructure()
        module.name = "MLPipeline"
        module.help = "Machine learning pipeline"
        module.location = "ml/pipeline.py"
        
        # Add module-level arguments (for __init__)
        init_arg = ArgumentStructure()
        init_arg.name_or_flags = "model_type"
        init_arg.dest = "model_type"
        init_arg.type = str
        init_arg.help = "Type of ML model"
        module.args.append(init_arg)
        
        # Create train command
        train_cmd = CommandStructure()
        train_cmd.name = "train"
        train_cmd.help = "Train the model"
        
        epochs_arg = ArgumentStructure()
        epochs_arg.name_or_flags = "epochs"
        epochs_arg.dest = "epochs"
        epochs_arg.type = int
        epochs_arg.help = "Number of training epochs"
        epochs_arg.default = 10
        train_cmd.args.append(epochs_arg)
        
        # Add decorator
        hydra_flag = DecoratorFlagStructure()
        hydra_flag.name = "add_hydra"
        hydra_flag.values = {"config_path": "conf", "config_name": "train"}
        train_cmd.decorator_flags.append(hydra_flag)
        
        module.commands.append(train_cmd)
        
        # Create predict command
        predict_cmd = CommandStructure()
        predict_cmd.name = "predict"
        predict_cmd.help = "Make predictions"
        
        input_arg = ArgumentStructure()
        input_arg.name_or_flags = "input_data"
        input_arg.dest = "input_data"
        input_arg.type = str
        input_arg.help = "Input data path"
        predict_cmd.args.append(input_arg)
        
        module.commands.append(predict_cmd)
        
        # Test serialization
        module_dict = module.to_dict()
        assert module_dict["name"] == "MLPipeline"
        assert len(module_dict["args"]) == 1
        assert len(module_dict["commands"]) == 2
        assert module_dict["commands"][0]["name"] == "train"
        assert len(module_dict["commands"][0]["decorator_flags"]) == 1
        
        # Test deserialization
        restored_module = ModuleStructure.from_dict(module_dict)
        assert restored_module.name == "MLPipeline"
        assert len(restored_module.args) == 1
        assert len(restored_module.commands) == 2

    def test_multiple_modules_collection(self):
        """Test creating a collection of multiple modules."""
        modules = ModuleStructures()
        
        # Module 1
        module1 = ModuleStructure()
        module1.name = "DataLoader"
        module1.help = "Load data"
        module1.location = "data/loader.py"
        module1.args = []
        
        cmd1 = CommandStructure()
        cmd1.name = "load"
        cmd1.help = "Load data from source"
        cmd1.args = []
        cmd1.decorator_flags = []
        module1.commands.append(cmd1)
        
        modules.modules.append(module1)
        
        # Module 2
        module2 = ModuleStructure()
        module2.name = "DataProcessor"
        module2.help = "Process data"
        module2.location = "data/processor.py"
        module2.args = []
        
        cmd2 = CommandStructure()
        cmd2.name = "process"
        cmd2.help = "Process loaded data"
        cmd2.args = []
        cmd2.decorator_flags = []
        module2.commands.append(cmd2)
        
        modules.modules.append(module2)
        
        # Test properties
        assert len(modules) == 2
        assert len(modules.names) == 2
        assert "DataLoader" in modules.names
        assert "DataProcessor" in modules.names
        
        locations = modules.locations
        assert locations["DataLoader"] == "data/loader.py"
        assert locations["DataProcessor"] == "data/processor.py"
        
        # Test full serialization cycle
        modules_dict = modules.to_dict()
        restored_modules = ModuleStructures.from_dict(modules_dict)
        
        assert len(restored_modules) == 2
        assert restored_modules.modules[0].name == "DataLoader"
        assert restored_modules.modules[1].name == "DataProcessor"
