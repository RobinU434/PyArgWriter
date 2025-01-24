from abc import ABC, abstractmethod
from ast import ClassDef, Dict, FunctionDef
import ast
import logging



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
        raise NotImplementedError
    
    @abstractmethod
    def get_arg_help_msg(self, node: FunctionDef) -> Dict[str, str]:
        raise NotImplementedError

    @abstractmethod
    def get_return_msg(self, node: FunctionDef) -> str:
        raise NotADirectoryError
    

class GoogleDocstringParser(DocstringParser):
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
        pass

        

        
    