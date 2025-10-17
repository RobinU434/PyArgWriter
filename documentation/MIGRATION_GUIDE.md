# Migration Guide: PyArgWriter → CLIfy v2.0.0

This guide will help you migrate from PyArgWriter (v1.x.x) to CLIfy (v2.0.0).

## Overview

CLIfy v2.0.0 represents a major rebranding of PyArgWriter with the following changes:
- Package name: `pyargwriter` → `clify`
- CLI command: `pyargwriter` → `clify`
- Import paths: `from pyargwriter` → `from clify`
- Logo and branding updates

**Timeline:**
- **Current**: PyArgWriter v1.x.x (stable)
- **v1.9.x**: Deprecation warnings introduced
- **v2.0.0**: Full CLIfy release with breaking changes

## What's Changing?

### 1. Package Installation

**Before (v1.x.x):**
```bash
pip install pyargwriter
```

**After (v2.0.0):**
```bash
pip install clify
```

**Note**: The PyPI package `pyargwriter` will remain available with deprecation warnings pointing to `clify`.

### 2. CLI Commands

**Before (v1.x.x):**
```bash
python -m pyargwriter generate-argparser --input myapp.py
pyargwriter generate-argparser --input myapp.py
```

**After (v2.0.0):**
```bash
python -m clify generate-argparser --input myapp.py
clify generate-argparser --input myapp.py
```

**Backward Compatibility**: `pyargwriter` command will remain as an alias in v2.0.0 with deprecation warnings.

### 3. Python Imports

**Before (v1.x.x):**
```python
from pyargwriter.entrypoint import ArgParseWriter
from pyargwriter.decorator import add_hydra
from pyargwriter._core.docstring_parser import DocstringParser
```

**After (v2.0.0):**
```python
from clify.entrypoint import ArgParseWriter
from clify.decorator import add_hydra
from clify._core.docstring_parser import DocstringParser
```

### 4. Configuration Files

If you have configuration files or scripts that reference `pyargwriter`, update them:

**Before:**
```yaml
# pyproject.toml
[tool.poetry.dependencies]
pyargwriter = "^1.1.4"
```

**After:**
```yaml
# pyproject.toml
[tool.poetry.dependencies]
clify = "^2.0.0"
```

## Migration Steps

### Step 1: Assess Your Usage

Identify all places where PyArgWriter is used:

```bash
# Search for imports
grep -r "from pyargwriter" .
grep -r "import pyargwriter" .

# Search for CLI usage in scripts
grep -r "pyargwriter" *.sh
grep -r "pyargwriter" *.py

# Check dependencies
cat requirements.txt | grep pyargwriter
cat pyproject.toml | grep pyargwriter
cat setup.py | grep pyargwriter
```

### Step 2: Create a Migration Branch

```bash
git checkout -b migrate-to-clify-v2
```

### Step 3: Update Dependencies

**requirements.txt:**
```diff
- pyargwriter>=1.1.4
+ clify>=2.0.0
```

**pyproject.toml (Poetry):**
```diff
[tool.poetry.dependencies]
- pyargwriter = "^1.1.4"
+ clify = "^2.0.0"
```

**setup.py:**
```diff
install_requires=[
-     "pyargwriter>=1.1.4",
+     "clify>=2.0.0",
]
```

### Step 4: Update Python Imports

Use automated tools or manual replacement:

**Automated (using sed):**
```bash
# Backup first!
find . -name "*.py" -type f -exec sed -i 's/from pyargwriter/from clify/g' {} +
find . -name "*.py" -type f -exec sed -i 's/import pyargwriter/import clify/g' {} +
```

**Manual replacement in your code:**
```python
# Find all occurrences and replace:
# pyargwriter → clify
```

### Step 5: Update CLI Commands

**In scripts:**
```bash
# .github/workflows/build.yml
# Before:
- pyargwriter generate-argparser --input myapp.py

# After:
- clify generate-argparser --input myapp.py
```

**In Makefiles:**
```makefile
# Before:
generate-cli:
	python -m pyargwriter generate-argparser --input src/myapp.py --output cli

# After:
generate-cli:
	python -m clify generate-argparser --input src/myapp.py --output cli
```

### Step 6: Update Documentation

- Update README.md
- Update CONTRIBUTING.md
- Update inline documentation
- Update user guides
- Update CI/CD configurations

### Step 7: Test Thoroughly

```bash
# Reinstall dependencies
pip install -r requirements.txt

# Run your test suite
pytest

# Test CLI commands
clify generate-argparser --help

# Test your generated CLIs
python -m your_app --help
```

### Step 8: Update Generated Code

If you've committed generated parser code, regenerate it with CLIfy:

```bash
# Regenerate all parser code
clify generate-argparser --input src/*.py --output cli --pretty
```

## Automated Migration Script

We provide a migration script to automate most changes:

```bash
# Download the migration script
curl -O https://raw.githubusercontent.com/RobinU434/PyArgWriter/main/scripts/migrate_to_clify.py

# Run with dry-run first
python migrate_to_clify.py --dry-run

# Apply changes
python migrate_to_clify.py --apply

# Review changes
git diff
```

**Script features:**
- Updates Python imports
- Updates dependency files
- Updates CLI commands in scripts
- Creates backup before applying changes
- Generates migration report

## Compatibility Mode

During the transition period, you can use both packages:

```python
# Compatibility shim (available in v1.9.x)
try:
    from clify.entrypoint import ArgParseWriter
except ImportError:
    from pyargwriter.entrypoint import ArgParseWriter
```

However, we recommend completing the migration to avoid confusion.

## Breaking Changes in v2.0.0

### Removed Features

None. All functionality from v1.x.x is preserved.

### Changed Behavior

1. **Import paths**: All imports must be updated
2. **Package name**: PyPI package name changed
3. **CLI command**: New primary command name

### New Features in v2.0.0

- Improved error messages
- Enhanced documentation
- Better CLI help messages
- New logo and branding
- Improved type hints

## Deprecation Warnings (v1.9.x)

In the last v1.x.x release (v1.9.x), deprecation warnings will be added:

```python
# This will show a warning:
from pyargwriter.entrypoint import ArgParseWriter

# Warning message:
# DeprecationWarning: 'pyargwriter' is deprecated and will be removed in v2.0.0. 
# Please use 'from clify.entrypoint import ArgParseWriter' instead.
```

## Common Issues and Solutions

### Issue 1: ModuleNotFoundError

**Error:**
```
ModuleNotFoundError: No module named 'pyargwriter'
```

**Solution:**
```bash
pip install clify
# Update imports in your code
```

### Issue 2: CLI Command Not Found

**Error:**
```
bash: pyargwriter: command not found
```

**Solution:**
```bash
# Use new command
clify generate-argparser --input myapp.py

# Or reinstall
pip install --upgrade clify
```

### Issue 3: Import Errors in Existing Code

**Error:**
```python
ImportError: cannot import name 'ArgParseWriter' from 'pyargwriter'
```

**Solution:**
Update all imports:
```python
# Before
from pyargwriter.entrypoint import ArgParseWriter

# After
from clify.entrypoint import ArgParseWriter
```

### Issue 4: Generated Code Still References PyArgWriter

**Solution:**
Regenerate all parser code with CLIfy:
```bash
clify generate-argparser --input src/*.py --output cli --pretty --force
```

## Testing Your Migration

### Checklist

- [ ] All dependencies updated in requirements.txt/pyproject.toml
- [ ] All Python imports updated
- [ ] All CLI commands updated in scripts
- [ ] All documentation updated
- [ ] CI/CD configurations updated
- [ ] Test suite passes
- [ ] Generated CLI works correctly
- [ ] No deprecation warnings
- [ ] All team members informed

### Test Commands

```bash
# 1. Verify installation
clify --version

# 2. Test help
clify --help
clify generate-argparser --help

# 3. Test generation
clify generate-argparser --input test_file.py --output test_output --pretty

# 4. Run test suite
pytest

# 5. Test generated CLI
python -m your_generated_cli --help
```

## Rollback Plan

If you encounter issues, you can rollback:

```bash
# Rollback to v1.x.x
pip install "pyargwriter>=1.1.4,<2.0.0"

# Restore previous code
git checkout main
git branch -D migrate-to-clify-v2
```

## Getting Help

If you need assistance with migration:

1. **Documentation**: Check the [official docs](https://github.com/RobinU434/PyArgWriter)
2. **Issues**: [Open an issue](https://github.com/RobinU434/PyArgWriter/issues) with the `migration` label
3. **Discussions**: Ask in [GitHub Discussions](https://github.com/RobinU434/PyArgWriter/discussions)
4. **Email**: Contact robin.uhrich@gmail.com

## Timeline

- **Q4 2024**: v1.9.x with deprecation warnings
- **Q1 2025**: v2.0.0-beta releases
- **Q2 2025**: v2.0.0 stable release
- **Q3 2025**: End of v1.x.x support (security fixes only)
- **Q4 2025**: PyArgWriter package deprecated on PyPI

## Contributing to Migration Tools

Help us improve the migration experience:

- Test the migration script
- Report migration issues
- Suggest improvements
- Contribute to documentation

---

## Quick Reference Card

| Aspect | v1.x.x (PyArgWriter) | v2.0.0 (CLIfy) |
|--------|---------------------|----------------|
| **Package** | `pyargwriter` | `clify` |
| **Installation** | `pip install pyargwriter` | `pip install clify` |
| **CLI Command** | `pyargwriter` | `clify` |
| **Import** | `from pyargwriter` | `from clify` |
| **Module** | `python -m pyargwriter` | `python -m clify` |

---

**Good luck with your migration! We're here to help if you need it.** 🚀
