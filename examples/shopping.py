"""
shopping - A Python module containing custom classes for a simple calculator and a shopping cart.

This module defines two classes:
    - Calculator: A simple calculator class for basic arithmetic operations.
    - ShoppingCart: A shopping cart class to manage items and calculate the total cost.

Usage:
    # Import the classes from the shopping module
    from shopping import Calculator, ShoppingCart

    # Create instances of the classes
    calc = Calculator()
    cart = ShoppingCart()

    # Use the Calculator to perform arithmetic operations
    result = calc.add(5, 3)
    print(result)  # Output: 8

    result = calc.subtract(10, 4)
    print(result)  # Output: 6

    # Manage the shopping cart
    cart.add_item("Apple", 1.0)
    cart.add_item("Banana", 0.8)
    cart.add_item("Milk", 2.5)

    cart.remove_item("Banana")

    total_cost = cart.calculate_total()
    print(f"Total cost: ${total_cost:.2f}")

This module provides convenient classes to handle calculations and shopping tasks, offering simple and reusable functionality for various Python projects.
"""


class Calculator:
    """
    A simple calculator class for basic arithmetic operations.

    Public Methods:
        add(a, b): Returns the sum of two numbers.

    Args:
        a (float): The first number.
        b (float): The second number.

    subtract(a, b): Returns the result of subtracting 'b' from 'a'.

    Args:
        a (float): The first number.
        b (float): The second number.

    Private Methods:
        _multiply(a, b): Returns the product of two numbers.

        Args:
            a (float): The first number.
            b (float): The second number.

        _divide(a, b): Returns the result of dividing 'a' by 'b'.

        Args:
            a (float): The dividend.
            b (float): The divisor.
    """
    def add(self, a:float, b: float):
        """Returns the sum of two numbers.

        Args:
            a (float): The first number.
            b (float): The second number.
        """
        return a + b

    def subtract(self, a, b):
        """Returns the result of subtracting 'b' from 'a'.

        Args:
            a (float): The first number.
            b (float): The second number.
        """
        return a - b

    def _multiply(self, a, b):
        """Returns the product of two numbers.

        Args:
            a (float): The first number.
            b (float): The second number.
        """
        return a * b

    def _divide(self, a, b):
        """Returns the result of dividing 'a' by 'b'.

        Args:
            a (float): The dividend.
            b (float): The divisor.

        Raises:
            ValueError: If the divisor 'b' is zero.
        """
        if b == 0:
            raise ValueError("Cannot divide by zero.")
        return a / b


class ShoppingCart:
    """
    A shopping cart class to manage items and calculate the total cost.

    Public Methods:
        add_item(item, price): Adds an item to the cart with its price.

        Args:
            item (str): The name of the item.
            price (float): The price of the item.

        remove_item(item): Removes an item from the cart.

        Args:
            item (str): The name of the item.

        calculate_total(): Calculates the total cost of all items in the cart.

    Private Methods:
        _get_discounted_price(price, discount): Applies a discount to the item price.

        Args:
            price (float): The original price of the item.
            discount (float): The discount percentage as a decimal.

        _apply_tax(price): Applies tax to the item price.

        Args:
            price (float): The original price of the item.

        Returns:
            float: The final price after applying tax.
    """

    def __init__(self, tax_rate: float):
        """Initialize the shopping cart.
        
        Args:
            tax_rate (float): rate for taxes
        """
        self.items = {}
        self.tax_rate = tax_rate

    def add_item(self, item, price):
        """Adds an item to the cart with its price.

        Args:
            item (str): The name of the item.
            price (float): The price of the item.
        """
        self.items[item] = price

    def remove_item(self, item):
        """Removes an item from the cart.

        Args:
            item (str): The name of the item.
        """
        if item in self.items:
            del self.items[item]

    def calculate_total(self):
        """Calculates the total cost of all items in the cart.

        Returns:
            float: The total cost including tax.
        """
        total_cost = sum(self.items.values())
        return self._apply_tax(total_cost)

    def _get_discounted_price(self, price, discount):
        """Applies a discount to the item price.

        Args:
            price (float): The original price of the item.
            discount (float): The discount percentage as a decimal.

        Returns:
            float: The final price after applying the discount.
        """
        return price - (price * discount)

    def _apply_tax(self, price):
        """Applies tax to the item price.

        Args:
            price (float): The original price of the item.

        Returns:
            float: The final price after applying tax.
        """
        return price + (price * self.tax_rate)

