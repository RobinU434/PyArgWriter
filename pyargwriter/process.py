import logging
from typing import Any, Dict, List
from pyargwriter.utils.code_generator import CodeGenerator
from pyargwriter.utils.code_parser import CodeParser
from pyargwriter.utils.decorator import overwrite_protection
from pyargwriter.utils.file_system import (
    create_directory,
    create_file,
    get_project_root_name,
    load_file_tree,
)
from pyargwriter.utils.formatter import BlackFormatter


class ArgParseWriter:
    """A utility class for parsing and generating code for argument parsing."""
    def __init__(self, force: bool = False, **kwargs) -> None:
        """Initialize ArgParseWriter instance.

        Args:
            force (bool, optional): Whether to force overwriting existing files. Defaults to False.
        """
        self._force = force

        self._parser = CodeParser()
        self._generator = CodeGenerator()

        self._formatter = BlackFormatter()

        self._arg_parse_structure: Dict[str, Any]

    def parse_code(self, files: List[str], output: str, **kwargs):
        """Parse given code classes and store them eventually in a given output file. 

        Args:
            files (List[str]): List of file paths containing code classes.
            output (str): Output directory for parsed code. If set to "." -> print to terminal
        """
        for file in files:
            tree = load_file_tree(file)
            self._parser.parse_tree(tree, file)

        self._arg_parse_structure = self._parser.modules

        # how to return values
        if output == ".":
            print(repr(self._arg_parse_structure))
        elif output is None:
            return
        else:
            self._parser.write(output)

    def write_code(self, file: str, output: str, pretty: bool = False, **kwargs):
        """Write parsed code to file.

        Args:
            file (str): Path to the file containing parsed code.
            output (str): Output directory for generated code.
            pretty (bool, optional): Whether to format the generated code. Defaults to False.
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
        """Generate parser from parsed code.

        Args:
            files (List[str]): List of file paths containing code classes.
            output (str): Output directory for generated code.
            pretty (bool, optional): Whether to format the generated code. Defaults to False.
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
