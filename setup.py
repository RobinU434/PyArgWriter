import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as req_file:
    requirements = req_file.read().splitlines()

setuptools.setup(
    name="pyargwriter",
    version="0.1.0",  # Update with the appropriate version number
    author="Robin Uhrich",
    description="A Python Argument Parser Setup Writer",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/RobinU434/PyArgWriter",  # Update with your GitHub repository URL
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",  # Specify Linux as the operating system
    ],
    python_requires=">=3.6",  # Update with your minimum Python version requirement
    install_requires=requirements,  # Use the dependencies from requirements.txt
    entry_points={
        "console_scripts": [
            "pyargwriter=pyargwriter.__main__:main",  # Update with your main script and module
        ],
    },
)
