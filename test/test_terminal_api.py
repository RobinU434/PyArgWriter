import subprocess


def test_terminal_api_for_package(setup_files):
    # call the test module just once with help just to have a look if the generating has worked out
    cmd = "python -m test.test_project --help"
    subprocess.run(cmd, shell=True, capture_output=True)


def test_terminal_api_generate_argparser(cleanup_tmp_dir):
    # call the test module just once with help just to have a look if the generating has worked out
    cmd = " pyargwriter parse-code --input test/test_project/tester.py --output test/tmp/out.yaml"
    subprocess.run(cmd, shell=True, capture_output=True)
    cmd = " pyargwriter parse-code --input test/test_project/tester.py --output test/tmp/out.yml"
    subprocess.run(cmd, shell=True, capture_output=True)


def test_terminal_api_package_parse_code(cleanup_tmp_dir):
    # call the test module just once with help just to have a look if the generating has worked out
    cmd = "python -m test.test_project --help"
    subprocess.run(cmd, shell=True, capture_output=True)


def test_terminal_api_package_write_code(cleanup_tmp_dir):
    # call the test module just once with help just to have a look if the generating has worked out
    cmd = "python -m test.test_project --help"
    subprocess.run(cmd, shell=True, capture_output=True)
