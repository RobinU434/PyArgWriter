import pytest
from pyargwriter.entrypoint import ArgParseWriter
from pyargwriter._core.code_generator import CodeGenerator
from pyargwriter._core.code_inspector import ModuleInspector
from pyargwriter.utils.file_system import load_file_tree


def test_code_parser(cleanup_tmp_dir):
    parser = ModuleInspector()
    file = "test/test_project/tester.py"
    tree = load_file_tree(file)
    parser.visit(tree, file)
    parser.write("test/tmp/out.yaml")
    parser.write("test/tmp/out.yml")
    parser.write("test/tmp/out.json")
    with pytest.raises(UnboundLocalError):
        parser.write("test/tmp/out.xyz")
    parser.modules.to_dict()

    repr(parser)
    print(parser.modules)


def test_code_generator(cleanup_tmp_dir):
    parser = ModuleInspector()
    file = "test/test_project/tester.py"
    tree = load_file_tree(file)
    parser.visit(tree, file)
    parser.write("test/tmp/out.yaml")
    parser.write("test/tmp/out.yml")
    parser.write("test/tmp/out.json")
    argument_tree = parser.modules.to_dict()

    generator = CodeGenerator()
    generator.from_dict(argument_tree, "test/temp/utils/parser.py")
    generator.write(
        setup_parser_path="test/tmp/utils/parser.py",
        main_path="test/tmp/__main__.py",
        force=True,
    )
    generator.from_yaml("test/tmp/out.yaml", "test/temp/utils/parser.py")
    generator.write(
        setup_parser_path="test/tmp/utils/parser.py",
        main_path="test/tmp/__main__.py",
        force=True,
    )
    generator.from_yaml("test/tmp/out.yml", "test/temp/utils/parser.py")
    generator.write(
        setup_parser_path="test/tmp/utils/parser.py",
        main_path="test/tmp/__main__.py",
        force=True,
    )
    generator.from_json("test/tmp/out.json", "test/temp/utils/parser.py")
    generator.write(
        setup_parser_path="test/tmp/utils/parser.py",
        main_path="test/tmp/__main__.py",
        force=True,
    )


def test_argument_parser_module(cleanup_tmp_dir):
    pyargwriter = ArgParseWriter(True)

    files = ["test/test_project/tester.py", "test/test_project/dummy_class.py"]
    pyargwriter.parse_code(files=files, output=None)
    pyargwriter.parse_code(files=files, output=".")
    pyargwriter.parse_code(files=files, output="test/tmp/test.yaml")
    pyargwriter.parse_code(files=files, output="test/tmp/test.yml")
    pyargwriter.parse_code(files=files, output="test/tmp/test.json")

    pyargwriter.write_code(file="test/tmp/test.yaml", output="test/tmp", pretty=True)
    pyargwriter.write_code(file="test/tmp/test.yml", output="test/tmp", pretty=True)
    pyargwriter.write_code(file="test/tmp/test.json", output="test/tmp", pretty=True)

    pyargwriter.generate_parser(files, "test/tmp", pretty=True)


def test_fail_class(cleanup_tmp_dir, caplog):
    pyargwriter = ArgParseWriter(True)

    files = ["test/test_project/fail_class.py"]
    # Does not fail anymore... made it more robust
    pyargwriter.parse_code(files=files, output=".")

    with pytest.raises(UnboundLocalError):
        pyargwriter.write_code(
            file="test/tmp/test.toml", output="test/tmp", pretty=True
        )
