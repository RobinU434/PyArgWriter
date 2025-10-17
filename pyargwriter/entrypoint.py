import logging
from typing import Any, Dict, List
from pyargwriter._core.code_generator import CodeGenerator
from pyargwriter._core.code_inspector import ModuleInspector
from pyargwriter.decorator import overwrite_protection
from pyargwriter.utils.file_system import (
    create_directory,
    create_file,
    get_project_root_name,
    load_file_tree,
)
from pyargwriter.utils.formatter import BlackFormatter


class ArgParseWriter:
    """A utility class for parsing Python code and generating ArgumentParser setups.

    This class provides a complete workflow for analyzing Python classes and their methods,
    extracting their signatures and docstrings, and generating corresponding argparse code.

    The workflow typically consists of three stages:
    1. Parse Python source files to extract class and method information
    2. Generate ArgumentParser setup code from the parsed structure
    3. Format and write the generated code to files

    Attributes:
        _force (bool): Whether to force overwrite existing files without prompting.
        _inspector (ModuleInspector): Inspects Python modules to extract structure.
        _generator (CodeGenerator): Generates argparse code from parsed structure.
        _formatter (BlackFormatter): Formats generated code with Black.
        _arg_parse_structure (Dict[str, Any]): Parsed module structure data.

    Example:
        >>> writer = ArgParseWriter(force=True)
        >>> writer.generate_parser(
        ...     files=['mymodule.py'],
        ...     output='./generated',
        ...     pretty=True
        ... )
    """

    def __init__(self, force: bool = False, docstring_format: str = "google", **kwargs) -> None:
        """Initialize ArgParseWriter instance.

        Args:
            force (bool, optional): Whether to force overwriting existing files without prompting.
                Defaults to False.
            docstring_format (str, optional): Format of docstrings in source files. Available formats:
                - "Epytext": Epytext style docstrings
                - "reST": reStructuredText style docstrings
                - "Google": Google style docstrings (default)
                - "Numpydoc": NumPy style docstrings
                Defaults to "google".
            **kwargs: Additional keyword arguments (currently unused, reserved for future extensions).
        """
        self._force = force

        self._inspector = ModuleInspector(docstring_format)
        self._generator = CodeGenerator()

        self._formatter = BlackFormatter()

        self._arg_parse_structure: Dict[str, Any]
    
    def parse_code(self, files: List[str], output: str, **kwargs):
        """Parse Python source files and extract class/method structures for ArgumentParser generation.

        This method analyzes Python source files, extracts class definitions, method signatures,
        and docstrings, then serializes the structure to a YAML or JSON file (or prints to console).

        Args:
            files (List[str]): List of Python file paths to parse. Each file should contain
                Python classes with properly documented methods.
            output (str): Output destination for parsed code structure. Options:
                - "." : Print structure to stdout
                - None : Return without writing (structure stored internally)
                - "<path>.yaml" or "<path>.yml" : Write to YAML file
                - "<path>.json" : Write to JSON file
            **kwargs: Additional keyword arguments passed through (reserved for future use).

        Example:
            >>> writer = ArgParseWriter()
            >>> writer.parse_code(
            ...     files=['module1.py', 'module2.py'],
            ...     output='structure.yaml'
            ... )
        """
        for file in files:
            tree = load_file_tree(file)
            self._inspector.visit(tree, file)

        self._arg_parse_structure = self._inspector.modules

        # how to return values
        if output == ".":
            print(repr(self._arg_parse_structure))
        elif output is None:
            return
        else:
            self._inspector.write(output)

    def write_code(self, file: str, output: str, pretty: bool = False, **kwargs):
        """Generate ArgumentParser Python code from a parsed structure file.

        This method reads a previously parsed structure file (YAML or JSON) and generates
        the corresponding Python code for setting up ArgumentParser, including:
        - utils/parser.py: ArgumentParser setup functions
        - __main__.py: Main entry point with argument parsing logic
        - __init__.py: Package initialization file

        Args:
            file (str): Path to the parsed structure file. Supported formats:
                - .yaml or .yml: YAML format structure file
                - .json: JSON format structure file
            output (str): Output directory where generated files will be created.
                The directory structure will be: <output>/utils/parser.py and <output>/__main__.py
            pretty (bool, optional): Whether to format generated code using Black formatter.
                Defaults to False.
            **kwargs: Additional keyword arguments passed through (reserved for future use).

        Example:
            >>> writer = ArgParseWriter(force=True)
            >>> writer.write_code(
            ...     file='structure.yaml',
            ...     output='./my_cli',
            ...     pretty=True
            ... )
        """
        file_type = file.split(".")[-1]
        match file_type:
            case "yaml":
                generator_method = self._generator.from_yaml
            case "yml":
                generator_method = self._generator.from_yaml
            case "json":
                generator_method = self._generator.from_json

        output = output.rstrip("/")
        generator_method(file, output + "/utils/parser.py")

        create_directory(output + "/utils")
        self._generator.write(
            setup_parser_path=output + "/utils/parser.py",
            main_path=output + "/__main__.py",
            force=self._force,
        )

        # create __init__.py ?
        init_path = output + "/__init__.py"
        self._create_init(path=init_path)

        if pretty:
            self._format_code(output)

    def generate_parser(
        self,
        files: List[str],
        output: str,
        pretty: bool = False,
        **kwargs,
    ):
        """Complete end-to-end workflow: parse Python files and generate ArgumentParser code.

        This method combines parse_code() and write_code() into a single operation, providing
        a streamlined workflow from Python source files directly to generated ArgumentParser code.

        The method will:
        1. Parse the Python source files to extract class/method structures
        2. Generate ArgumentParser setup code
        3. Create necessary directory structure
        4. Write utils/parser.py, __main__.py, and __init__.py files
        5. Optionally format the code with Black

        Args:
            files (List[str]): List of Python source file paths to parse. Each file should
                contain Python classes with properly documented methods following the
                specified docstring format.
            output (str): Output directory where generated files will be created.
                The method will create the directory if it doesn't exist.
            pretty (bool, optional): Whether to format generated code using Black formatter
                for consistent style. Defaults to False.
            **kwargs: Additional keyword arguments passed through (reserved for future use).

        Example:
            >>> writer = ArgParseWriter(docstring_format='google')
            >>> writer.generate_parser(
            ...     files=['src/calculator.py', 'src/converter.py'],
            ...     output='./cli_app',
            ...     pretty=True
            ... )
            # Generated files:
            # - cli_app/utils/parser.py
            # - cli_app/__main__.py
            # - cli_app/__init__.py
        """
        self.parse_code(files, None)
        output = output.rstrip("/")
        project_root_name = get_project_root_name(output)
        self._generator.from_dict(
            self._arg_parse_structure.to_dict(), project_root_name + "/utils/parser.py"
        )

        create_directory(output + "/utils")
        self._generator.write(
            setup_parser_path=output + "/utils/parser.py",
            main_path=output + "/__main__.py",
            force=self._force,
        )

        # create __init__.py ?
        init_path = output + "/__init__.py"
        self._create_init(path=init_path)

        if pretty:
            self._format_code(output)

    def _format_code(
        self,
        *files,
    ):
        """Format code using BlackFormatter."""
        msg = f"Format code with {type(self._formatter).__name__}"
        logging.info(msg)
        self._formatter.format(files)

    def _create_init(self, path):
        """Create '__init__.py' file in the specified path."""
        if self._force:
            create_file(path)
        else:

            @overwrite_protection
            def wrapper(path):
                create_file(path)

            wrapper(path=path)
