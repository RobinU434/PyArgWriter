import logging
import re
import subprocess


def check_pylint(path: str) -> bool:
    print("Check: ", path)
    error_codes_regex = "E[0-9][0-9][0-9][0-9]:"
    fatal_codes_regex = "F[0-9][0-9][0-9][0-9]:"

    command = f"pylint {path}"
    result = subprocess.run(command, shell=True, capture_output=True)
    # run(..., check=True, stdout=PIPE).stdout
    result = result.stdout.decode("utf-8")
    error_messages = re.findall(error_codes_regex, str(result))

    # Ignore unable to import errors
    try:
        error_messages.remove("E0401:")
    except ValueError:
        pass
    num_error_messages = len(error_messages)

    num_fatal_messages = len(re.findall(fatal_codes_regex, str(result)))
    print("Num error messages: ", num_error_messages)
    print("Num fatal messages: ", num_fatal_messages)
    print(result)
    return not(num_error_messages or num_fatal_messages)


def check_run(path: str):
    modules = ".".join(path[:-3].split("/"))
    command = f"python -m {modules} --help"
    print(command)
    result = subprocess.run(command, shell=True, capture_output=True)
    print("stdout: ", result.stdout.decode("utf-8"))
    print("stderr: ", result.stderr.decode("utf-8"))
    std_err = result.stderr.decode("utf-8")

    return not len(re.findall("Traceback", std_err))

