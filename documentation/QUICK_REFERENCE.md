# CLIfy Quick Reference Card

Quick commands and patterns for CLIfy (CLI Forge for Python)

---

## Installation

```bash
# Current (PyArgWriter)
pip install pyargwriter

# Future (CLIfy v2.0.0)
pip install clify
```

---

## CLI Commands

### One-Stop Generation (Recommended)
```bash
# Current
clify generate-argparser --input myapp.py --output . --pretty
python -m pyargwriter generate-argparser --input myapp.py --output . --pretty

# Multiple files
clify generate-argparser --input app.py utils.py --output ./cli --pretty

# With logging
clify generate-argparser --input myapp.py --log-level DEBUG
```

### Two-Step Process
```bash
# Step 1: Extract structure
clify parse-code --input myapp.py --output structure.yaml

# Step 2: Generate code
clify write-code --input structure.yaml --output . --pretty
```

---

## Python Class Template

### Minimal Example
```python
class MyApp:
    """Brief description of your app."""
    
    def command(self, arg: str):
        """Command description.
        
        Args:
            arg (str): Argument description
        """
        pass
```

### Complete Example
```python
class DataProcessor:
    """Process data files with various operations."""
    
    def process(
        self,
        input_file: str,
        output_format: str = "json",
        verbose: bool = False,
        batch_size: int = 100,
        tags: list[str] = None
    ):
        """Process input file and convert to specified format.
        
        Args:
            input_file (str): Path to input data file
            output_format (str): Output format (json, csv, xml). Defaults to json.
            verbose (bool): Enable verbose logging. Defaults to False.
            batch_size (int): Number of records per batch. Defaults to 100.
            tags (list[str]): List of tags to apply. Defaults to None.
        
        Returns:
            dict: Processing results with status and output path
        """
        pass
```

---

## Supported Types

| Type | Example | CLI Usage |
|------|---------|-----------|
| `int` | `count: int` | `--count 42` |
| `float` | `ratio: float` | `--ratio 3.14` |
| `str` | `name: str` | `--name "text"` |
| `bool` | `verbose: bool` | `--verbose` (flag) |
| `list[int]` | `ids: list[int]` | `--ids 1 2 3` |
| `list[float]` | `values: list[float]` | `--values 1.5 2.5` |
| `list[str]` | `names: list[str]` | `--names a b c` |
| `List[int]` | `from typing import List` | `--ids 1 2 3` |

---

## Docstring Formats

### Google (Default)
```python
def func(arg: str):
    """Description.
    
    Args:
        arg (str): Description
    
    Returns:
        str: Description
    """
```

### NumPy
```python
def func(arg: str):
    """
    Description.
    
    Parameters
    ----------
    arg : str
        Description
    
    Returns
    -------
    str
        Description
    """
```

### reStructuredText
```python
def func(arg: str):
    """
    Description.
    
    :param arg: Description
    :type arg: str
    :return: Description
    :rtype: str
    """
```

### Epydoc
```python
def func(arg: str):
    """
    Description.
    
    @param arg: Description
    @type arg: str
    @return: Description
    @rtype: str
    """
```

---

## Python API

```python
from pyargwriter.entrypoint import ArgParseWriter

# Create writer
writer = ArgParseWriter(
    pretty=True,                    # Format with Black
    force=True,                     # Overwrite existing
    docstring_format="google"       # google, numpy, rest, epytext
)

# Generate parser
writer.generate_parser(
    files=["myapp.py"],
    output="."
)

# Two-step process
writer.parse_code(files=["myapp.py"], output="structure.yaml")
writer.write_code(structure_file="structure.yaml", output=".")
```

---

## Hydra Integration

```python
from omegaconf import DictConfig
from pyargwriter.decorator import add_hydra

class Pipeline:
    @add_hydra("config", version_base=None)
    def train(self, config: DictConfig, device: str = "cuda"):
        """Train model.
        
        Args:
            config (DictConfig): Hydra configuration
            device (str): Training device
        """
        pass
```

Usage:
```bash
python -m pipeline train --device cpu --config-name my_config
```

---

## Generated CLI Usage

After generation, use your CLI:

```bash
# Help
python -m myapp --help
python -m myapp command --help

# Run commands
python -m myapp command --arg value
python -m myapp command --flag
python -m myapp command --list-arg 1 2 3
```

---

## Common Patterns

### Multiple Methods
```python
class App:
    """App with multiple commands."""
    
    def start(self, port: int = 8000):
        """Start server."""
        pass
    
    def stop(self, force: bool = False):
        """Stop server."""
        pass
```

Usage:
```bash
python -m app start --port 3000
python -m app stop --force
```

### Default Values
```python
def process(
    self,
    timeout: int = 30,      # --timeout 30 (default)
    retries: int = 3,       # --retries 3 (default)
    validate: bool = True   # --validate (default True)
):
    """Process with defaults."""
    pass
```

### List Arguments
```python
def batch_process(
    self,
    files: list[str],           # --files a.txt b.txt c.txt
    ids: list[int] = None,      # --ids 1 2 3 (optional)
):
    """Process multiple files."""
    pass
```

---

## Debugging

### Verbose Output
```bash
clify generate-argparser --input myapp.py --log-level DEBUG
```

### Check Generated Files
```bash
# Generated structure
cat ./utils/parser.py

# Check imports
head -20 ./__main__.py
```

### Test Generated CLI
```bash
# Check if it works
python -m myapp --help

# Try with arguments
python -m myapp command --arg test
```

---

## Error Messages

| Error | Cause | Solution |
|-------|-------|----------|
| `No module named 'pyargwriter'` | Not installed | `pip install pyargwriter` |
| `Missing docstring` | No docstring | Add docstring to function |
| `Type annotation missing` | No type hint | Add `: type` to argument |
| `Module not found` | Wrong path | Check `--input` path |
| `Permission denied` | No write access | Check `--output` directory |

---

## Best Practices

1. **Always add type hints**: `arg: str` not just `arg`
2. **Write clear docstrings**: Help users understand your CLI
3. **Use default values**: Make arguments optional when sensible
4. **Format code**: Use `--pretty` flag for clean output
5. **Test after generation**: Run `python -m myapp --help`
6. **Document defaults**: Mention default values in docstrings
7. **Use descriptive names**: `input_file` not `inp`
8. **Group related commands**: Use classes to organize functionality

---

## Examples Directory

```
examples/
├── shopping.py          # E-commerce CLI
├── car.py              # Vehicle management
└── ml_pipeline.py      # ML training with Hydra
```

Run examples:
```bash
clify generate-argparser --input examples/shopping.py --output examples --pretty
python -m examples.shopping --help
```

---

## Help & Support

- **Documentation**: [Full docs](https://github.com/RobinU434/PyArgWriter)
- **Examples**: [DOCSTRING_FORMAT_EXAMPLES.md](DOCSTRING_FORMAT_EXAMPLES.md)
- **Issues**: [GitHub Issues](https://github.com/RobinU434/PyArgWriter/issues)
- **Email**: robin.uhrich@gmail.com

---

## Version Info

- **Current**: v1.x.x (as `pyargwriter`)
- **Next**: v2.0.0 (rebranding to `clify`)
- **Python**: >= 3.10, < 4.0
- **Docstring Formats**: 4 (Google, NumPy, reST, Epydoc)

---

**Print this card and keep it handy!** 📋
