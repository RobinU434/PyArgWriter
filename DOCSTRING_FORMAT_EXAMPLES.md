# Docstring Format Examples for PyArgWriter

This document provides comprehensive examples of all supported docstring formats in PyArgWriter.

## Supported Formats

PyArgWriter now supports four major Python docstring formats:
1. **Google Style** - Google's Python Style Guide format
2. **Epydoc Style** - Epydoc/Javadoc-like format with @ tags
3. **reStructuredText (ReST)** - Sphinx/reStructuredText format with : fields
4. **NumPy Style** - NumPy/SciPy documentation standard

---

## 1. Google Style (Default)

### Basic Example
```python
class DataProcessor:
    """Process and analyze data.
    
    This class provides methods for data processing and analysis.
    """
    
    def process(self, data, validate=True):
        """Process the input data.
        
        Args:
            data (list): Input data to process.
            validate (bool): Whether to validate data before processing.
                Defaults to True.
        
        Returns:
            dict: Processed data with metadata.
        
        Raises:
            ValueError: If data is invalid and validate is True.
        """
        return {"data": data, "validated": validate}
```

### Usage
```python
from pyargwriter.entrypoint import ArgParseWriter

writer = ArgParseWriter()
writer.generate_parser(
    files=["mymodule.py"],
    output=".",
    docstring_format="google"  # This is the default
)
```

---

## 2. Epydoc Style

### Basic Example
```python
class DataProcessor:
    """
    Process and analyze data.
    
    This class provides methods for data processing and analysis.
    """
    
    def process(self, data, validate=True):
        """
        Process the input data.
        
        @param data: Input data to process.
        @type data: list
        @param validate: Whether to validate data before processing.
            Defaults to True.
        @type validate: bool
        @return: Processed data with metadata.
        @rtype: dict
        @raise ValueError: If data is invalid and validate is True.
        """
        return {"data": data, "validated": validate}
```

### Advanced Example with Multiple Parameters
```python
def calculate(x, y, operation, precision=2):
    """
    Perform mathematical calculation on two numbers.
    
    @param x: First operand for the calculation.
    @type x: float
    @param y: Second operand for the calculation.
    @type y: float
    @param operation: Type of operation ('add', 'subtract', 'multiply', 'divide').
    @type operation: str
    @param precision: Number of decimal places in result. Defaults to 2.
    @type precision: int
    @return: Result of the calculation rounded to specified precision.
    @rtype: float
    """
    pass
```

### Usage
```python
writer.generate_parser(
    files=["mymodule.py"],
    output=".",
    docstring_format="epytext"
)
```

---

## 3. reStructuredText (ReST/Sphinx) Style

### Basic Example
```python
class DataProcessor:
    """
    Process and analyze data.
    
    This class provides methods for data processing and analysis.
    """
    
    def process(self, data, validate=True):
        """
        Process the input data.
        
        :param data: Input data to process.
        :type data: list
        :param validate: Whether to validate data before processing.
            Defaults to True.
        :type validate: bool
        :return: Processed data with metadata.
        :rtype: dict
        :raises ValueError: If data is invalid and validate is True.
        """
        return {"data": data, "validated": validate}
```

### Advanced Example with Cross-References
```python
def train_model(features, labels, epochs=10, learning_rate=0.01):
    """
    Train a machine learning model.
    
    :param features: Input feature matrix.
    :type features: numpy.ndarray
    :param labels: Target labels for training.
    :type labels: numpy.ndarray
    :param epochs: Number of training epochs. Defaults to 10.
    :type epochs: int
    :param learning_rate: Learning rate for optimization. Defaults to 0.01.
    :type learning_rate: float
    :return: Trained model with weights and training history.
    :rtype: dict
    :raises ValueError: If features and labels have mismatched dimensions.
    """
    pass
```

### Usage
```python
writer.generate_parser(
    files=["mymodule.py"],
    output=".",
    docstring_format="rest"
)
```

---

## 4. NumPy Style

### Basic Example
```python
class DataProcessor:
    """
    Process and analyze data.
    
    This class provides methods for data processing and analysis.
    """
    
    def process(self, data, validate=True):
        """
        Process the input data.
        
        Parameters
        ----------
        data : list
            Input data to process.
        validate : bool, optional
            Whether to validate data before processing.
            Defaults to True.
        
        Returns
        -------
        dict
            Processed data with metadata containing:
            - data: The processed data
            - validated: Whether validation was performed
        
        Raises
        ------
        ValueError
            If data is invalid and validate is True.
        """
        return {"data": data, "validated": validate}
```

### Advanced Example with Complex Types
```python
def analyze_timeseries(
    data,
    window_size=10,
    method='rolling_mean',
    fill_na=True
):
    """
    Analyze time series data with various methods.
    
    Parameters
    ----------
    data : pandas.DataFrame or numpy.ndarray
        Time series data to analyze. If DataFrame, must have
        DatetimeIndex. If ndarray, assumed to be sequential.
    window_size : int, optional
        Size of the rolling window for analysis.
        Defaults to 10.
    method : {'rolling_mean', 'exponential', 'savgol'}, optional
        Analysis method to apply to the data.
        Defaults to 'rolling_mean'.
    fill_na : bool, optional
        Whether to fill NaN values with interpolation.
        Defaults to True.
    
    Returns
    -------
    pandas.DataFrame
        Analyzed time series with the following columns:
        - original: Original data values
        - analyzed: Analyzed/smoothed values
        - residuals: Difference between original and analyzed
    
    Raises
    ------
    ValueError
        If window_size is larger than the data length.
    TypeError
        If data is not a supported type.
    
    Notes
    -----
    This function uses pandas rolling window operations for
    efficient computation. For large datasets, consider
    chunking the data.
    
    Examples
    --------
    >>> import pandas as pd
    >>> data = pd.DataFrame({'value': [1, 2, 3, 4, 5]})
    >>> result = analyze_timeseries(data, window_size=3)
    >>> print(result['analyzed'])
    """
    pass
```

### Usage
```python
writer.generate_parser(
    files=["mymodule.py"],
    output=".",
    docstring_format="numpydoc"
)
```

---

## Comparison Table

| Feature | Google | Epydoc | ReST | NumPy |
|---------|--------|--------|------|-------|
| Readability | 5/5 | 3/5 | 4/5 | 5/5 |
| Compactness | 5/5 | 3/5 | 3/5 | 2/5 |
| Sphinx Support | 3/5 | 2/5 | 5/5 | 5/5 |
| IDE Support | 5/5 | 3/5 | 4/5 | 4/5 |
| Verbosity | Low | Medium | Medium | High |
| Best For | General use | Java devs | Sphinx docs | Scientific |

---

## Mixed Format Example (Not Recommended)

While PyArgWriter supports multiple formats, **it's strongly recommended to use a single format consistently** throughout your project. However, PyArgWriter will handle mixed formats:

```python
# File: myproject/module1.py (Google style)
class GoogleStyleClass:
    """A class using Google style.
    
    Args:
        param1 (str): Description.
    """
    pass

# File: myproject/module2.py (NumPy style)  
class NumpyStyleClass:
    """
    A class using NumPy style.
    
    Parameters
    ----------
    param1 : str
        Description.
    """
    pass
```

When processing mixed formats, specify the primary format:

```python
# Will attempt to parse each file with the specified format
writer.generate_parser(
    files=["myproject/module1.py", "myproject/module2.py"],
    output=".",
    docstring_format="google"  # Primary format
)
```

---

## Best Practices

### 1. Consistency is Key
Choose one format and stick with it across your entire project.

### 2. Include Type Hints
While PyArgWriter extracts types from annotations, docstrings provide additional context:

```python
def process(data: list[str], validate: bool = True) -> dict:
    """Process data with validation.
    
    Args:
        data: List of strings to process. Type annotation in signature.
        validate: Enable validation. Defaults to True.
    
    Returns:
        Processed data dictionary.
    """
    pass
```

### 3. Document Defaults
Always document default parameter values:

```python
def configure(timeout=30, retries=3):
    """
    Configure connection settings.
    
    Parameters
    ----------
    timeout : int, optional
        Connection timeout in seconds. Defaults to 30.
    retries : int, optional
        Number of retry attempts. Defaults to 3.
    """
    pass
```

### 4. Be Descriptive
Provide meaningful descriptions, not just type information:

```python
# ❌ Bad
def process(data):
    """
    Process data.
    
    Args:
        data: The data.
    
    Returns:
        The result.
    """
    pass

# ✅ Good
def process(data):
    """
    Normalize and validate input data for machine learning.
    
    Args:
        data (pandas.DataFrame): Raw input data containing features
            and labels. Must have columns 'X' and 'y'.
    
    Returns:
        pandas.DataFrame: Normalized data with mean=0 and std=1,
            ready for model training.
    """
    pass
```

---

## Converting Between Formats

If you need to convert existing docstrings from one format to another, consider using tools like:

- **pyment**: Converts between different docstring styles
- **docformatter**: Formats docstrings to PEP 257
- **pydocstyle**: Checks docstring style compliance

Example conversion workflow:
```bash
# Convert from NumPy to Google style
pyment -w -o google mymodule.py

# Then generate ArgumentParser with PyArgWriter
pyargwriter generate mymodule.py --output . --format google
```

---

## Testing Your Docstrings

After writing docstrings, test that PyArgWriter parses them correctly:

```python
from pyargwriter._core.docstring_parser import DocstringParser
import ast

# Load your module
with open("mymodule.py") as f:
    tree = ast.parse(f.read())

# Get a function node
func_node = tree.body[0]

# Test parsing
parser = DocstringParser.build_parser("google")  # or "epytext", "rest", "numpydoc"
help_msg = parser.get_help_msg(func_node)
arg_help = parser.get_arg_help_msg(func_node)

print(f"Help: {help_msg}")
print(f"Arguments: {arg_help}")
```

---

## Summary

- **Google Style**: Best for general Python projects, most readable
- **Epydoc Style**: Good for teams familiar with Javadoc
- **ReST Style**: Best for Sphinx documentation
- **NumPy Style**: Best for scientific/data science projects

Choose based on your team's preferences and existing documentation standards!
