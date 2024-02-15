import subprocess


def test_terminal_api():
    # call the test module just once with help just to have a look if the generating has worked out
    cmd = "python -m test.test_project --help"
    subprocess.run(cmd, shell=True, capture_output=True)
