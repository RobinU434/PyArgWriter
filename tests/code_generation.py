import os
import re
import subprocess

from pyargwriter.code_generator import Main, SetupParser
from pyargwriter.utils.decorator import cleanup_tests

COMMAND_DATA = {
        'commands': [
            {
                'name': 'command1',
                'help': 'Help for command1',
                'args': [
                    {
                        'dest': 'arg1',
                        'type': 'str',
                        'help': 'Help for arg1',
                        # 'required': True,
                        'default': None
                    },
                    {
                        'dest': 'arg2',
                        'type': 'int',
                        'help': 'Help for arg2',
                        # 'required': False,
                        'default': 0
                    }
                ]
            },
            {
                'name': 'command2',
                'help': 'Help for command2',
                'args': [
                    {
                        'dest': 'option1',
                        'type': 'bool',
                        'help': 'Help for option1',
                        # 'required': False,
                        'default': False
                    },
                    {
                        'dest': 'option2',
                        'type': 'str',
                        'help': 'Help for option2',
                        # 'required': True,
                        'default': 'default_value'
                    }
                ]
            },
            {
                'name': 'command3',
                'help': 'Help for command3',
                'args': [
                    {
                        'dest': 'arg3',
                        'type': 'list',
                        'help': 'Help for arg3',
                        # 'required': True,
                        'default': []
                    },
                    {
                        'dest': 'arg4',
                        'type': 'dict',
                        'help': 'Help for arg4',
                        # 'required': False,
                        'default': {}
                    }
                ]
            }
        ]
    }

PROJECT_PATH = subprocess.check_output("pwd", shell=True).decode("utf-8")[:-1]


@cleanup_tests
def test_run_completion():
    func = SetupParser(COMMAND_DATA['commands'])
    func.write("./tests/temp/test.py")
    main = Main()
    main.write("./tests/temp/test_main.py")
    # os.system("rm tests/temp/*.py")


@cleanup_tests
def test_check_generated_code_for_errors():
    func = SetupParser(COMMAND_DATA['commands'])
    func.write("./tests/temp/test.py")
    main = Main("test.py")
    main.write("./tests/temp/test_main.py")
    
    error_codes_regex = "E[0-9][0-9][0-9][0-9]:"
    fatal_codes_regex = "F[0-9][0-9][0-9][0-9]:"
    
    command = f"pylint {PROJECT_PATH}/tests/temp/test.py"
    result = subprocess.run(command, shell=True, capture_output=True)
    # run(..., check=True, stdout=PIPE).stdout
    result = result.stdout.decode("utf-8")
    assert(len(re.findall(error_codes_regex, str(result))) == 0)
    assert(len(re.findall(fatal_codes_regex, str(result))) == 0)

    command = f"pylint {PROJECT_PATH}/tests/temp/test_main.py"
    result = subprocess.run(command, shell=True, capture_output=True)
    assert(len(re.findall(error_codes_regex, str(result))) == 0)
    assert(len(re.findall(fatal_codes_regex, str(result))) == 0)


@cleanup_tests
def test_is_runable():
    func = SetupParser(COMMAND_DATA['commands'])
    func.write("./tests/temp/test.py")
    main = Main("tests/temp/test.py")
    main.write("./tests/temp/test_main.py")
    
    result = subprocess.run(f"python -m tests.temp.test_main --help", shell=True, capture_output=True)
    std_err = result.stderr.decode("utf-8")

    assert(len(re.findall("Traceback", std_err)) == 0)
