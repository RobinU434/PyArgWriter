# PyArgWriter

[![Coverage Status](https://coveralls.io/repos/github/RobinU434/PyArgWriter/badge.svg?branch=main)](https://coveralls.io/github/RobinU434/PyArgWriter?branch=main)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pyargwriter)
![PyPI - Downloads](https://img.shields.io/pypi/dm/pyargwriter)
![PyPI - Version](https://img.shields.io/pypi/v/pyargwriter)

PyArgWriter is a Python module that simplifies the generation of ArgumentParser setups for Python classes and their methods. It provides a convenient way to define and manage command-line arguments for your Python applications.

## Installation

You can install PyArgWriter using `pip`:

```bash
pip install pyargwriter
```

Alternative from source code:

In root folder with pip:

```bash
pip install .
```

or with poetry:

```bash
poetry install
```

## Command-Line Interface

PyArgWriter offers the following command-line commands:

- `parse-code`: Parse given files and create YAML structure with structural parser information.
- `write-code`: Read given parser YAML structure and create argument parser Python code.
- `generate-argparser`: Generate `parser.py`, which contains a `setup_parser` function to set up an appropriate parser.

For more detailed information on available command-line arguments and usage examples, refer to the official documentation.

## Requirements

PyArgWriter depends strongly on information stated in the docstring. Your docstring should have a minimal structure like:

```python       
def add(a: int, b: int) -> int:
    """_summary_

    Args:
        a (int): _description_
        b (int): _description_

    Returns:
        int: _description_
    """
    return a + b
```

## Usage

Usage
PyArgWriter offers a command-line interface for generating and managing ArgumentParser setups.
Below are the available commands and their usage:

### parse-code

```bash
python -m pyargwriter parse-code --input file1.py file2.py --output output.yaml [--log-level LOG_LEVEL]
```

Parse given Python files and create a YAML structure with structural parser information.

### write-code

```bash
python -m pyargwriter write-code --input input.yaml [--output OUTPUT_DIR] [--pretty] [--log-level LOG_LEVEL]
```

Read a given parser YAML structure and generate argument parser Python code.

### generate-argparser

```bash
python -m pyargwriter generate-argparser --input file1.py file2.py [--output OUTPUT_DIR] [--pretty] [--log-level LOG_LEVEL]
```

Generate a parser.py file that contains a setup_parser function to set up an appropriate ArgumentParser.
Common Options
--log-level LOG_LEVEL: Sets the log level for command execution (default is "WARN").
--pretty (-p): If set, the generated code will be formatted with Black.
For more detailed information on each command and additional options, run:

```bash
python -m pyargwriter <command> --help
```

### Supported Argument Types

In the function of the process class you want to create the argument parser, following types of an argument are supported:

- int
- float
- str
- bool flags
- list[int]
- List[int]     # from typing
- list[float]
- List[float]   # from typing
- list[str]
- List[str]     # from typing
- list[bool]
- List[bool]    # from typing

## Example

```bash
python -m pyargwriter generate-argparser --input examples/shopping.py examples/car.py --output examples --pretty
```

## Hydra Integration

As an additional feature we support to combine your existing `ArgumentParser` with the [Hydra](https://hydra.cc/docs/intro/) framework. All you need to do is to use a decorator we provide with our framework. A short example can be viewed below. 

```python
from omegaconf import DictConfig
from pyargwriter.decorator import add_hydra

class Entrypoint:
    """ML training pipeline"""
    def __init__(self):
        """initiate pipeline"""
        pass
    @add_hydra("config", version_base=None)
    def train(config: DictConfig, device: str):
        """start training process
        
        Args:
            config (DictConfig): container which contains
            device (str): where to train on
        """
```
The decorator is indeed callable. Additionally to the usual hydra-arguments you have to pass in the `config_var_name` which specifies which argument in the `train` signature is the config object. After calling the pyargwriter tool you are now ready to go with a CLI which can now handle also almost all Hydra commands. Except the normal `help` message you get from Hydra. For further interest in this message please refer to their [website](https://hydra.cc/docs/intro/)


## Documentation

The complete documentation for PyArgWriter, including detailed usage instructions and examples, can be found in the [official documentation](documentation/latex/refman.pdf) or at the [documentation website](https://htmlpreview.github.io/?https://github.com/RobinU434/PyArgWriter/blob/main/documentation/html/index.htm).

Further you can have a look into the [test coverage](documentation/test_coverage.md).

## License

This project is licensed under the Apache 2.0 License - see the [LICENSE](LICENSE) file for details.

## Contributing

If you would like to contribute to PyArgWriter, please read our [Contributing Guidelines](CONTRIBUTING.md) for details on how to get started.

## Contact

For any questions, issues, or feedback, please [open an issue](https://github.com/RobinU434/PyArgWriter/issues) on our GitHub repository.


## Ideas for Naming

Here are some potential names for your tool, focusing on its functionality and the concept of automatically generating CLI interfaces:

### Functional and Descriptive Names
1. **AutoCLI**
2. **ClassCLI**
3. **MethodCLI**
4. **CLIBuilder**
5. **ArgParserGen**
6. **ClassParser**
7. **Method2CLI**
8. **CLIForge**

### Playful and Catchy Names
1. **CLImate** (a nod to "CLI" and "automate")
2. **CLIonize** (like ionizing a class into a CLI)
3. **CLIckIt** (emphasizing ease and speed)
4. **Parse-o-Matic**
5. **Argonaut** (exploring arguments and generating interfaces)

### Tech-Inspired Names
1. **CommandCrafter**
2. **InterfaceSmith**
3. **AutoArg**
4. **PyCLI**
5. **CodeCommander**

### Generalized and Creative Names
1. **Argitect** (argument architect)
2. **CommandWeaver**
3. **ParseMaster**
4. **CLIMaker**
5. **MethodBridge**

Each of these names is tailored to different branding styles. Do you have preferences about whether the name should be more functional, playful, or tech-inspired?

If you want the name to be short, easy to type, and terminal-friendly, here are some concise options:

1. **cli-gen**
2. **argen** (short for "argument generator")
3. **clify**
4. **m2cli** (short for "method to CLI")
5. **pycli**
6. **cligen**
7. **argcli**
8. **cly** (a super-short take on "CLI")
9. **cmdgen**
10. **methcli** (short for "method CLI")
11  . **clipy**

These names are minimal, straightforward, and easy to remember for developers. Let me know if any of these stand out!