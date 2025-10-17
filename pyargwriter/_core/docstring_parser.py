from abc import ABC, abstractmethod
from ast import ClassDef, FunctionDef
import ast
import logging
import re
from typing import Dict


class DocstringParser(ABC):
    default_help_msg = "--no-documentation-exists--"

    def __init__(self):
        super().__init__()

    def _check_for_docstring(self, node: FunctionDef):
        doc_str = ast.get_docstring(node)
        if doc_str is None:
            msg = f"No docstring for method {node.name} available"
            logging.fatal(msg)
            error_msg = f"Process was aborted because of missing doc-string in function: {node.name}"
            raise ValueError(error_msg)

    @abstractmethod
    def get_help_msg(self, node: FunctionDef | ClassDef) -> str:
        """get first line of docstring

        Args:
            node (FunctionDef | ClassDef): ast object to extract docstring from

        Returns:
            str: first line of docstring
        """
        raise NotImplementedError

    @abstractmethod
    def get_arg_help_msg(self, node: FunctionDef) -> Dict[str, str]:
        """get key value pairs of arg_name and its help message

        Args:
            node (FunctionDef): where to extract the docstring from

        Returns:
            Dict[str, str]: arg_name: help message
        """
        raise NotImplementedError

    @abstractmethod
    def get_return_msg(self, node: FunctionDef) -> str:
        """get help message of return type

        Args:
            node (FunctionDef): where to extract docstring from

        Returns:
            str: help message of return type
        """
        raise NotImplementedError

    @classmethod
    def build_parser(cls, docstring_format: str) -> "DocstringParser":
        class_dict = {
            "epytext": EpyTextParser,
            "rest": ReSTParser,
            "google": GoogleParser,
            "numpydoc": NumpyDocParser,
        }
        return class_dict[docstring_format.lower()]()


class GoogleParser(DocstringParser):
    def __init__(self):
        super().__init__()

    def get_help_msg(self, node):
        docstring = ast.get_docstring(node)
        if docstring is None:
            logging.info(f"No docstring in {node.name} found.")
            msg = self.default_help_msg
        else:
            msg = docstring.split("\n")[0]

        return msg

    def get_arg_help_msg(self, node):
        docstring = ast.get_docstring(node)
        num_args = len(node.args.args)
        if num_args == 0:
            return dict()
        elif num_args == 1 and node.args.args[0].arg == "self":
            return dict()

        # if there is no documentation
        if docstring is None:
            keys = [arg.arg for arg in node.args.args]
            if "self" in keys:
                keys.remove("self")
            values = [self.default_help_msg] * len(keys)
            res = dict(zip(keys, values))
            return res

        # if there is a sufficient docstring -> extract message
        docstring: list[str] = docstring.split("\n")
        args_start = docstring.index("Args:")
        res = {}
        for idx in range(args_start + 1, args_start + num_args):
            splits = docstring[idx].strip(" ").split(":")
            arg = splits[0]
            # delete bracket with type information
            arg = re.sub(r"\(.*?\)", "", arg).strip(" ")
            msg = ":".join(splits[1:]).strip(" ")
            res[arg] = msg
        return res

    def get_return_msg(self, node):
        return super().get_return_msg(node)


class EpyTextParser(DocstringParser):
    """Parser for Epydoc-style docstrings.
    
    Format:
        @param arg_name: description
        @type arg_name: type
        @return: description
        @rtype: return_type
    """
    
    def __init__(self):
        super().__init__()

    def get_help_msg(self, node):
        """Extract first line of docstring for Epydoc format.
        
        Args:
            node: AST node (FunctionDef or ClassDef)
            
        Returns:
            str: First line of docstring or default message
        """
        docstring = ast.get_docstring(node)
        if docstring is None:
            logging.info(f"No docstring in {node.name} found.")
            return self.default_help_msg
        
        # Get first line before any @param tags
        lines = docstring.split("\n")
        for line in lines:
            stripped = line.strip()
            if stripped and not stripped.startswith("@"):
                return stripped
        
        return self.default_help_msg

    def get_arg_help_msg(self, node):
        """Extract argument help messages from Epydoc format.
        
        Args:
            node: FunctionDef AST node
            
        Returns:
            Dict[str, str]: Mapping of argument names to help messages
        """
        docstring = ast.get_docstring(node)
        num_args = len(node.args.args)
        
        if num_args == 0:
            return dict()
        elif num_args == 1 and node.args.args[0].arg == "self":
            return dict()
        
        # if there is no documentation
        if docstring is None:
            keys = [arg.arg for arg in node.args.args]
            if "self" in keys:
                keys.remove("self")
            values = [self.default_help_msg] * len(keys)
            return dict(zip(keys, values))
        
        # Parse @param tags
        lines = docstring.split("\n")
        res = {}
        
        for line in lines:
            stripped = line.strip()
            if stripped.startswith("@param "):
                # Format: @param arg_name: description
                match = re.match(r"@param\s+(\w+):\s*(.*)", stripped)
                if match:
                    arg_name = match.group(1)
                    description = match.group(2)
                    res[arg_name] = description if description else self.default_help_msg
        
        # Fill in missing arguments with default message
        for arg in node.args.args:
            if arg.arg != "self" and arg.arg not in res:
                res[arg.arg] = self.default_help_msg
        
        return res

    def get_return_msg(self, node):
        """Extract return message from Epydoc format.
        
        Args:
            node: FunctionDef AST node
            
        Returns:
            str: Return description or default message
        """
        docstring = ast.get_docstring(node)
        if docstring is None:
            return self.default_help_msg
        
        lines = docstring.split("\n")
        for line in lines:
            stripped = line.strip()
            if stripped.startswith("@return:") or stripped.startswith("@returns:"):
                # Format: @return: description
                match = re.match(r"@returns?:\s*(.*)", stripped)
                if match:
                    description = match.group(1)
                    return description if description else self.default_help_msg
        
        return self.default_help_msg


class ReSTParser(DocstringParser):
    """Parser for reStructuredText (Sphinx) style docstrings.
    
    Format:
        :param arg_name: description
        :type arg_name: type
        :return: description
        :rtype: return_type
    """
    
    def __init__(self):
        super().__init__()

    def get_help_msg(self, node):
        """Extract first line of docstring for ReST format.
        
        Args:
            node: AST node (FunctionDef or ClassDef)
            
        Returns:
            str: First line of docstring or default message
        """
        docstring = ast.get_docstring(node)
        if docstring is None:
            logging.info(f"No docstring in {node.name} found.")
            return self.default_help_msg
        
        # Get first line before any :param tags
        lines = docstring.split("\n")
        for line in lines:
            stripped = line.strip()
            if stripped and not stripped.startswith(":"):
                return stripped
        
        return self.default_help_msg

    def get_arg_help_msg(self, node):
        """Extract argument help messages from ReST format.
        
        Args:
            node: FunctionDef AST node
            
        Returns:
            Dict[str, str]: Mapping of argument names to help messages
        """
        docstring = ast.get_docstring(node)
        num_args = len(node.args.args)
        
        if num_args == 0:
            return dict()
        elif num_args == 1 and node.args.args[0].arg == "self":
            return dict()
        
        # if there is no documentation
        if docstring is None:
            keys = [arg.arg for arg in node.args.args]
            if "self" in keys:
                keys.remove("self")
            values = [self.default_help_msg] * len(keys)
            return dict(zip(keys, values))
        
        # Parse :param tags
        lines = docstring.split("\n")
        res = {}
        
        for line in lines:
            stripped = line.strip()
            if stripped.startswith(":param "):
                # Format: :param arg_name: description
                match = re.match(r":param\s+(\w+):\s*(.*)", stripped)
                if match:
                    arg_name = match.group(1)
                    description = match.group(2)
                    res[arg_name] = description if description else self.default_help_msg
        
        # Fill in missing arguments with default message
        for arg in node.args.args:
            if arg.arg != "self" and arg.arg not in res:
                res[arg.arg] = self.default_help_msg
        
        return res

    def get_return_msg(self, node):
        """Extract return message from ReST format.
        
        Args:
            node: FunctionDef AST node
            
        Returns:
            str: Return description or default message
        """
        docstring = ast.get_docstring(node)
        if docstring is None:
            return self.default_help_msg
        
        lines = docstring.split("\n")
        for line in lines:
            stripped = line.strip()
            if stripped.startswith(":return:") or stripped.startswith(":returns:"):
                # Format: :return: description
                match = re.match(r":returns?:\s*(.*)", stripped)
                if match:
                    description = match.group(1)
                    return description if description else self.default_help_msg
        
        return self.default_help_msg


class NumpyDocParser(DocstringParser):
    """Parser for NumPy-style docstrings.
    
    Format:
        Parameters
        ----------
        arg_name : type
            description
        
        Returns
        -------
        return_type
            description
    """
    
    def __init__(self):
        super().__init__()

    def get_help_msg(self, node):
        """Extract first line of docstring for NumPy format.
        
        Args:
            node: AST node (FunctionDef or ClassDef)
            
        Returns:
            str: First line of docstring or default message
        """
        docstring = ast.get_docstring(node)
        if docstring is None:
            logging.info(f"No docstring in {node.name} found.")
            return self.default_help_msg
        
        # Get first line before Parameters section
        lines = docstring.split("\n")
        for line in lines:
            stripped = line.strip()
            if stripped and stripped not in ["Parameters", "Returns", "-" * len(stripped)]:
                return stripped
        
        return self.default_help_msg

    def get_arg_help_msg(self, node):
        """Extract argument help messages from NumPy format.
        
        Args:
            node: FunctionDef AST node
            
        Returns:
            Dict[str, str]: Mapping of argument names to help messages
        """
        docstring = ast.get_docstring(node)
        num_args = len(node.args.args)
        
        if num_args == 0:
            return dict()
        elif num_args == 1 and node.args.args[0].arg == "self":
            return dict()
        
        # if there is no documentation
        if docstring is None:
            keys = [arg.arg for arg in node.args.args]
            if "self" in keys:
                keys.remove("self")
            values = [self.default_help_msg] * len(keys)
            return dict(zip(keys, values))
        
        # Parse Parameters section
        lines = docstring.split("\n")
        res = {}
        
        in_params_section = False
        current_arg = None
        current_description = []
        
        for i, line in enumerate(lines):
            stripped = line.strip()
            
            # Check if we're entering Parameters section
            if stripped == "Parameters":
                # Next line should be dashes
                if i + 1 < len(lines) and lines[i + 1].strip().startswith("-"):
                    in_params_section = True
                continue
            
            # Check if we're leaving Parameters section
            if in_params_section and stripped in ["Returns", "Raises", "Examples", "Notes"]:
                if current_arg:
                    res[current_arg] = " ".join(current_description).strip() or self.default_help_msg
                break
            
            if in_params_section and stripped and not stripped.startswith("-"):
                # Check if this is a parameter line (contains :)
                if ":" in stripped:
                    # Save previous parameter
                    if current_arg:
                        res[current_arg] = " ".join(current_description).strip() or self.default_help_msg
                    
                    # Parse new parameter: arg_name : type
                    parts = stripped.split(":", 1)
                    current_arg = parts[0].strip()
                    current_description = []
                else:
                    # This is a description line
                    if current_arg:
                        current_description.append(stripped)
        
        # Save last parameter
        if current_arg:
            res[current_arg] = " ".join(current_description).strip() or self.default_help_msg
        
        # Fill in missing arguments with default message
        for arg in node.args.args:
            if arg.arg != "self" and arg.arg not in res:
                res[arg.arg] = self.default_help_msg
        
        return res

    def get_return_msg(self, node):
        """Extract return message from NumPy format.
        
        Args:
            node: FunctionDef AST node
            
        Returns:
            str: Return description or default message
        """
        docstring = ast.get_docstring(node)
        if docstring is None:
            return self.default_help_msg
        
        lines = docstring.split("\n")
        in_returns_section = False
        description_lines = []
        
        for i, line in enumerate(lines):
            stripped = line.strip()
            
            # Check if we're entering Returns section
            if stripped == "Returns":
                # Next line should be dashes
                if i + 1 < len(lines) and lines[i + 1].strip().startswith("-"):
                    in_returns_section = True
                continue
            
            # Check if we're leaving Returns section
            if in_returns_section and stripped in ["Raises", "Examples", "Notes", "Parameters"]:
                break
            
            # Collect description lines
            if in_returns_section and stripped and not stripped.startswith("-"):
                description_lines.append(stripped)
        
        if description_lines:
            # Skip the first line if it looks like a type annotation
            if len(description_lines) > 1:
                return " ".join(description_lines[1:]).strip() or self.default_help_msg
            return description_lines[0] or self.default_help_msg
        
        return self.default_help_msg
