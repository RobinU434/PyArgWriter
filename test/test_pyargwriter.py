import unittest
from argparse import ArgumentParser, Namespace
from unittest.mock import Mock, patch
from pyargwriter.utils.log_level import set_log_level
from pyargwriter.utils.parser import (
    setup_parser,
    add_general_args,
    add_writer_args,
    add_generate_parser_args,
)
from pyargwriter.main import execute


class TestPyArgWriter(unittest.TestCase):
    def setUp(self):
        self.log_level_args = ["--log-level", "DEBUG"]
        self.input_args = ["--input", "examples/shopping.py"]
        self.output_args = ["--output", "output_file.txt"]
        self.pretty_args = ["--pretty"]
        self.force_args = ["--force"]

    def test_set_log_level(self):
        set_log_level("DEBUG")
        # Add assertions to check if the log level is set correctly

    def test_setup_parser(self):
        parser = ArgumentParser()
        setup_parser(parser)
        # Add assertions to check if the parser is set up correctly

    def test_add_general_args(self):
        parser = ArgumentParser()
        parser = add_general_args(parser)
        args = parser.parse_args(self.log_level_args)
        self.assertEqual(args.log_level, "DEBUG")
        # Add more assertions to check other arguments

    def test_add_writer_args(self):
        parser = ArgumentParser()
        parser = add_writer_args(parser)
        args = parser.parse_args(
            self.input_args + self.output_args + self.pretty_args + self.force_args
        )
        self.assertEqual(args.file, "examples/shopping.py")
        self.assertEqual(args.output, "output_file.txt")
        self.assertTrue(args.pretty)
        self.assertTrue(args.force)

    def test_add_generate_parser_args(self):
        parser = ArgumentParser()
        parser = add_generate_parser_args(parser)
        args = parser.parse_args(
            self.input_args + self.output_args + self.pretty_args + self.force_args
        )
        self.assertEqual(args.files, ["examples/shopping.py"])
        self.assertEqual(args.output, "output_file.txt")
        self.assertTrue(args.pretty)
        self.assertTrue(args.force)

    def test_ArgParseWriter_parse_code(self):
        # Mock ArgParseWriter and its methods
        args = Namespace(
                command="parse-code", log_level="DEBUG", files=["examples/shopping.py"], output="test/temp/structure.yaml"
            )
        execute(vars(args))

        args.output = "test/temp/structure.yml"
        execute(vars(args))

        args.output = "test/temp/structure.json"
        execute(vars(args))


    def test_ArgParseWriter_write_code(self):
        # create structure to write code from
        args = Namespace(
                command="parse-code", log_level="DEBUG", files=["examples/shopping.py"], output="test/temp/structure.yaml"
            )
        execute(vars(args))

        args = Namespace(
                command="write-code",
                log_level="DEBUG",
                file="test/temp/structure.yaml",
                output="test/temp",
                pretty=True,
                force=True,
            )
        execute(vars(args))

    def test_ArgParseWriter_generate_parser(self):
        # Mock ArgParseWriter and its methods

        args = Namespace(
                command="generate-argparser",
                log_level="DEBUG",
                files=["examples/shopping.py"],
                output="test/temp",
                pretty=True,
                force=True,
            )
        execute(vars(args))


    def test_ArgParseWriter_unknown_command(self):
        # Mock ArgParseWriter and its methods
        args = Namespace(command="unknown-command")
        try:
            execute(vars(args))
        except KeyError:
            pass
            

if __name__ == "__main__":
    unittest.main()
