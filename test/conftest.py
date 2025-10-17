import glob
import os
import pytest
from clify.entrypoint import ArgParseWriter


def pytest_addoption(parser):
    parser.addoption("--keep-files", action="store_true")


def run_pyargwriter():
    writer = ArgParseWriter(force=True)
    input_file = "test/test_project/tester.py"
    output = "test/test_project"
    writer.generate_parser(files=[input_file], output=output, pretty=True)


def cleanup_generated_files():
    base_dir = "test/test_project"
    files_to_remove = ["__init__.py", "__main__.py", "utils/parser.py"]
    files_to_remove = [base_dir + "/" + file for file in files_to_remove]

    for file in files_to_remove:
        os.remove(file)


@pytest.fixture(scope="session")
def setup_files(request: pytest.FixtureRequest) -> None:
    run_pyargwriter()
    if not request.config.getoption("--keep-files"):
        request.addfinalizer(cleanup_generated_files)


@pytest.fixture(scope="session")
def cleanup_tmp_dir(request: pytest.FixtureRequest) -> None:
    def cleanup():
        yaml_files = glob.glob("test/tmp/*.yaml")
        yml_files = glob.glob("test/tmp/*.yml")
        json_files = glob.glob("test/tmp/*.json")
        python_files = glob.glob("test/tmp/*.py")
        emb_python_files = glob.glob("test/tmp/*/*.py")

        files = [*yaml_files, *yml_files, *json_files, *python_files, *emb_python_files]

        for file in files:
            os.remove(file)

    if not request.config.getoption("--keep-files"):
        request.addfinalizer(cleanup)
