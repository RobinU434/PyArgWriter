import subprocess

from test.utils import stderr_is_relevant


def test_terminal_api_for_package(setup_files):
    # call the test module just once with help just to have a look if the generating has worked out
    cmd = "python -m test.test_project --help"
    result = subprocess.run(cmd, cwd="test", shell=True, capture_output=True)
    assert not stderr_is_relevant(result.stderr.decode())


def test_terminal_api_package_parse_code_one_class(cleanup_tmp_dir):
    # call the test module just once with help just to have a look if the generating has worked out
    cmd = "python -m test.test_project --help"
    cmd = " pyargwriter parse-code --input test/test_project/tester.py --output test/tmp/out.yaml"
    result = subprocess.run(cmd, shell=True, capture_output=True)
    assert not stderr_is_relevant(result.stderr.decode())
    cmd = " pyargwriter parse-code --input test/test_project/tester.py --output test/tmp/out.yml"
    result = subprocess.run(cmd, shell=True, capture_output=True)
    assert not stderr_is_relevant(result.stderr.decode())
    cmd = "pyargwriter parse-code --input test/test_project/tester.py --output test/tmp/out.json"
    result = subprocess.run(cmd, shell=True, capture_output=True)
    assert not stderr_is_relevant(result.stderr.decode())
    cmd = "pyargwriter parse-code --input test/test_project/tester.py --output ."
    result = subprocess.run(cmd, shell=True, capture_output=True)
    assert not stderr_is_relevant(result.stderr.decode())


def test_terminal_api_package_parse_code_multiple_classes(cleanup_tmp_dir):
    # call the test module just once with help just to have a look if the generating has worked out
    cmd = " pyargwriter parse-code --input test/test_project/tester.py test/test_project/dummy_class.py --output test/tmp/out.yaml"
    result = subprocess.run(cmd, shell=True, capture_output=True)
    assert not stderr_is_relevant(result.stderr.decode())
    cmd = " pyargwriter parse-code --input test/test_project/tester.py test/test_project/dummy_class.py --output test/tmp/out.yml"
    result = subprocess.run(cmd, shell=True, capture_output=True)
    assert not stderr_is_relevant(result.stderr.decode())
    cmd = "pyargwriter parse-code --input test/test_project/tester.py test/test_project/dummy_class.py --output test/tmp/out.json"
    result = subprocess.run(cmd, shell=True, capture_output=True)
    assert not stderr_is_relevant(result.stderr.decode())
    cmd = "pyargwriter parse-code --input test/test_project/tester.py test/test_project/dummy_class.py --output ."
    result = subprocess.run(cmd, shell=True, capture_output=True)
    assert not stderr_is_relevant(result.stderr.decode())


def test_terminal_api_package_write_code(cleanup_tmp_dir):
    # call the test module just once with help just to have a look if the generating has worked out
    cmd = "pyargwriter parse-code --input test/test_project/tester.py --output test/tmp/out.yaml"
    result = subprocess.run(cmd, shell=True, capture_output=True)
    assert not stderr_is_relevant(result.stderr.decode())
    cmd = (
        "pyargwriter write-code --input test/tmp/out.yaml --output test/tmp --pretty -f"
    )
    result = subprocess.run(cmd, shell=True, capture_output=True)
    assert not stderr_is_relevant(result.stderr.decode())
    cmd = (
        "pyargwriter write-code --input test/tmp/out.yaml --output test/tmp --pretty -f"
    )
    result = subprocess.run(cmd, shell=True, capture_output=True)
    assert not stderr_is_relevant(result.stderr.decode())


def test_terminal_api_package_write_code_multiple_classes(cleanup_tmp_dir):
    # call the test module just once with help just to have a look if the generating has worked out
    cmd = "pyargwriter write-code --input test/tmp/out.yaml --output test/tmp -f"
    result = subprocess.run(cmd, shell=True, capture_output=True)
    assert not stderr_is_relevant(result.stderr.decode())
    cmd = (
        "pyargwriter write-code --input test/tmp/out.yaml --output test/tmp --pretty -f"
    )
    result = subprocess.run(cmd, shell=True, capture_output=True)
    assert not stderr_is_relevant(result.stderr.decode())
    cmd = (
        "pyargwriter write-code --input test/tmp/out.yml --output test/tmp --pretty  -f"
    )
    result = subprocess.run(cmd, shell=True, capture_output=True)
    assert not stderr_is_relevant(result.stderr.decode())
    cmd = (
        "pyargwriter write-code --input test/tmp/out.json --output test/tmp --pretty -f"
    )
    result = subprocess.run(cmd, shell=True, capture_output=True)
    assert not stderr_is_relevant(result.stderr.decode())
