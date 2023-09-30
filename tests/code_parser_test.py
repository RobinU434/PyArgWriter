import ast
from pyargwriter.utils.code_parser import CodeParser


MODULES = {
    "modules": [
        {
            'name': 'Calculator',
            'help': '',
            'commands': [
                {
                    'name': 'add', 
                    'help': 'Returns the sum of two numbers.',
                    'args': [
                        {'dest': 'a', 'help': 'The first number.', 'type': 'float'},
                        {'dest': 'b', 'help': 'The second number.', 'type': 'float'}
                        ]
                    },
                {
                    'name': 'subtract',
                    'help': "Returns the result of subtracting 'b' from 'a'.",
                    'args': [
                        {'dest': 'a', 'help': 'The first number.'}, 
                        {'dest': 'b', 'help': 'The second number.'}
                        ]
                }
            ]
        }, 
        {
            'name': 'ShoppingCart', 
            'help': '',
            'commands': [
                {
                    'name': 'add_item', 
                    'help': 'Adds an item to the cart with its price.', 
                    'args': [
                        {'dest': 'item', 'help': 'The name of the item.'},
                        {'dest': 'price', 'help': 'The price of the item.'}
                    ]
                },
                {
                    'name': 'remove_item',
                    'help': 'Removes an item from the cart.',
                    'args': [
                        {'dest': 'item', 'help': 'The name of the item.'}
                    ]
                },
                {
                    'name': 'calculate_total',
                    'help': 'Calculates the total cost of all items in the cart.',
                    'args': []
                }
            ]
        }
    ]
}


def test_run_completion():
    func = CodeParser()

    # load tree
    with open("examples/shopping.py", 'r') as file:
        tree = ast.parse(file.read())
    
    func.parse_tree(tree)

    assert func.modules.to_dict() == MODULES

def test_write_yaml():
    func = CodeParser()

    # load tree
    with open("examples/shopping.py", 'r') as file:
        tree = ast.parse(file.read())
    
    func.parse_tree(tree)
    func.write("tests/temp/test.yaml")
    func.write("tests/temp/test.yml")

def test_write_json():
    func = CodeParser()

    # load tree
    with open("examples/shopping.py", 'r') as file:
        tree = ast.parse(file.read())
    
    func.parse_tree(tree)
    func.write("tests/temp/test.json")

