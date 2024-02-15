"""In this function we will call the ArgumentTester from a simulated command-line and test if the typing test function will detect an error"""

import subprocess
from test import (
    INT,
    STR,
    FLOAT,
)


def test_int(setup_files):
    a = INT
    b = INT
    cmd = f"python -m test.test_project int-test --a {a}"
    subprocess.run(cmd, shell=True, check=True)
    cmd = f"python -m test.test_project int-test --a {a} --b {b}"
    subprocess.run(cmd, shell=True, check=True)


def test_str(setup_files):
    a = STR
    b = STR
    cmd = f"python -m test.test_project str-test --a {a}"
    subprocess.run(cmd, shell=True, check=True)
    cmd = f"python -m test.test_project str-test --a {a} --b {b}"
    subprocess.run(cmd, shell=True, check=True)


def test_float(setup_files):
    a = FLOAT
    b = FLOAT
    cmd = f"python -m test.test_project float-test --a {a}"
    subprocess.run(cmd, shell=True, check=True)
    cmd = f"python -m test.test_project float-test --a {a} --b {b}"
    subprocess.run(cmd, shell=True, check=True)


def test_bool_false(setup_files):
    cmd = "python -m test.test_project bool-false-test"
    subprocess.run(cmd, shell=True, check=True)
    cmd = "python -m test.test_project bool-false-test --b"
    subprocess.run(cmd, shell=True, check=True)


def test_bool_true(setup_files):
    cmd = "python -m test.test_project bool-true-test --a"
    subprocess.run(cmd, shell=True, check=True)
    cmd = "python -m test.test_project bool-true-test --a --b"
    subprocess.run(cmd, shell=True, check=True)
