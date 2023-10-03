# PyArgWriter

PyArgWriter is a Python module that simplifies the generation of ArgumentParser setups for Python classes and their methods. It provides a convenient way to define and manage command-line arguments for your Python applications.

## Installation

You can install PyArgWriter using `pip`:

```bash
pip install pyargwriter
```

## Command-Line Interface

PyArgWriter offers the following command-line commands:

- `parse-code`: Parse given files and create YAML structure with structural parser information.
- `write-code`: Read given parser YAML structure and create argument parser Python code.
- `generate-argparser`: Generate `parser.py`, which contains a `setup_parser` function to set up an appropriate parser.

For more detailed information on available command-line arguments and usage examples, refer to the official documentation.

## Usage

Usage
PyArgWriter offers a command-line interface for generating and managing ArgumentParser setups. Below are the available commands and their usage:

### parse-code

``` bash
python -m pyargwriter parse-code --input file1.py file2.py --output output.yaml [--log-level LOG_LEVEL]
```

Parse given Python files and create a YAML structure with structural parser information.

### write-code

``` bash
python -m pyargwriter write-code --input input.yaml [--output OUTPUT_DIR] [--pretty] [--log-level LOG_LEVEL]
```

Read a given parser YAML structure and generate argument parser Python code.

### generate-argparser

``` bash
python -m pyargwriter generate-argparser --input file1.py file2.py [--output OUTPUT_DIR] [--pretty] [--log-level LOG_LEVEL]
```

Generate a parser.py file that contains a setup_parser function to set up an appropriate ArgumentParser.
Common Options
--log-level LOG_LEVEL: Sets the log level for command execution (default is "WARN").
--pretty (-p): If set, the generated code will be formatted with Black.
For more detailed information on each command and additional options, run:

``` bash
python -m pyargwriter <command> --help
```

## Documentation

The complete documentation for PyArgWriter, including detailed usage instructions and examples, can be found in the [official documentation](documentation/latex/refman.pdf). To look into the html version open: `documentation/html/index.html` in your browser

## License

This project is licensed under the Apache 2.0 License - see the [LICENSE](LICENSE) file for details.

## Contributing

If you would like to contribute to PyArgWriter, please read our [Contributing Guidelines](CONTRIBUTING.md) for details on how to get started.

## Contact

For any questions, issues, or feedback, please [open an issue](https://github.com/RobinU434/pyargwriter/issues) on our GitHub repository.
