import subprocess

PROJECT_PATH = subprocess.check_output("pwd", shell=True).decode("utf-8")[:-1]

