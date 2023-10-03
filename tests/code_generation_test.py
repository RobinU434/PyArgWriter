import logging
import re
import subprocess

from pyargwriter.utils.code_generator import CodeGenerator, MainFunc, SetupParser
from pyargwriter.utils.decorator import cleanup_tests
from tests.utils.checks import check_pylint, check_run
from tests import PROJECT_PATH

import sys
sys.path.append(PROJECT_PATH + "/tests")
sys.path.append(PROJECT_PATH + "/tests/temp")
print(sys.path)

MODULES = {
    "modules": [
        {
            "name": "Calculator",
            "help": "",
            "commands": [
                {
                    "name": "add",
                    "help": "Returns the sum of two numbers.",
                    "args": [
                        {
                            "dest": "a",
                            "help": "The first number.",
                            "type": "float"
                        }, 
                        {
                            "dest": "b",
                            "help": "The second number.",
                            "type": "float"
                        }
                    ]
                },
                {
                    "name": "subtract",
                    "help": "Returns the result of subtracting 'b' from 'a'.",
                    "args": [
                        {
                            "dest": "a",
                            "help": "The first number."
                        },
                        {
                            "dest": "b",
                            "help": "The second number."
                        }
                    ]
                }
            ]
        },
        {
            "name": "ShoppingCart",
            "help": "",
            "commands": [
                {
                    "name": "add_item",
                    "help": "Adds an item to the cart with its price.",
                    "args": [
                        {
                            "dest": "item",
                            "help": "The name of the item."
                        },
                        {
                            "dest": "price",
                            "help": "The price of the item."
                        }
                    ]
                },
                {
                    "name": "remove_item",
                    "help": "Removes an item from the cart.",
                    "args": [
                        {
                            "dest": "item",
                            "help": "The name of the item."
                        }
                    ]
                },
                {
                    "name": "calculate_total",
                    "help": "Calculates the total cost of all items in the cart.",
                    "args": []
                }
            ]
        }
    ]
}

@cleanup_tests
def test_run_single_module_from_dict():
    print(sys.path)
    setup_parser_path = "./tests/temp/test.py"
    main_path = "./tests/temp/test_main.py"
    # single class
    generator = CodeGenerator()
    data = {"modules": [MODULES["modules"][0]]}
    generator.from_dict(data, "tests/temp/test.py")
    generator.write(setup_parser_path, main_path)
    # os.system("rm tests/temp/*.py")
    assert check_pylint(f"{PROJECT_PATH}/tests/temp/test.py")
    assert check_pylint(f"{PROJECT_PATH}/tests/temp/test_main.py")
    
    assert check_run("tests/temp/test_main.py")

@cleanup_tests
def test_multiple_modules_from_dict():
    setup_parser_path = "./tests/temp/test.py"
    main_path = "./tests/temp/test_main.py"
    generator = CodeGenerator()
    generator.from_dict(MODULES, "tests.temp.test.py")
    generator.write(setup_parser_path, main_path)
    assert check_pylint(f"{PROJECT_PATH}/tests/temp/test.py")
    assert check_pylint(f"{PROJECT_PATH}/tests/temp/test_main.py")

    assert check_run("tests/temp/test_main.py")

@cleanup_tests
def test_single_modules_from_yaml():
    setup_parser_path = "./tests/temp/test.py"
    main_path = "./tests/temp/test_main.py"
    yaml_path = "./tests/data/test_single.yaml"
    generator = CodeGenerator()
    generator.from_yaml(yaml_path, "tests.temp.test.py")
    generator.write(setup_parser_path, main_path)
    assert check_pylint(f"{PROJECT_PATH}/tests/temp/test.py")
    assert check_pylint(f"{PROJECT_PATH}/tests/temp/test_main.py")

    assert check_run("tests/temp/test_main.py")


@cleanup_tests
def test_multiple_modules_from_yaml():
    setup_parser_path = "./tests/temp/test.py"
    main_path = "./tests/temp/test_main.py"
    yaml_path = "./tests/data/test_multi.yaml"
    generator = CodeGenerator()
    generator.from_yaml(yaml_path, "tests.temp.test.py")
    generator.write(setup_parser_path, main_path)
    assert check_pylint(f"{PROJECT_PATH}/tests/temp/test.py")
    assert check_pylint(f"{PROJECT_PATH}/tests/temp/test_main.py")

    assert check_run("tests/temp/test_main.py")


@cleanup_tests
def test_single_modules_from_json():
    setup_parser_path = "./tests/temp/test.py"
    main_path = "./tests/temp/test_main.py"
    json_path = "./tests/data/test_single.json"
    generator = CodeGenerator()
    generator.from_json(json_path, "tests.temp.test.py")
    generator.write(setup_parser_path, main_path)
    assert check_pylint(f"{PROJECT_PATH}/tests/temp/test.py")
    assert check_pylint(f"{PROJECT_PATH}/tests/temp/test_main.py")
    
    assert check_run("tests/temp/test_main.py")


def test_multiple_modules_from_json():
    setup_parser_path = "./tests/temp/test.py"
    main_path = "./tests/temp/test_main.py"
    json_path = "./tests/data/test_multi.json"
    generator = CodeGenerator()
    generator.from_json(json_path, "tests.temp.test.py")
    generator.write(setup_parser_path, main_path)
    assert check_pylint(f"{PROJECT_PATH}/tests/temp/test.py")
    assert check_pylint(f"{PROJECT_PATH}/tests/temp/test_main.py")

    assert check_run("tests/temp/test_main.py")

