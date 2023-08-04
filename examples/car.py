"""
shopping.py - A Python module containing custom classes for a car and a bank account.

This module defines two classes:
    - Car: A class representing a car with methods to start the engine.
    - BankAccount: A class representing a bank account with methods to deposit and withdraw money.

Usage:
    # Import the classes from the shopping module
    from shopping import Car, BankAccount

    # Create instances of the classes
    car = Car("Toyota", "Camry", 2022, fuel_type="Petrol")
    account = BankAccount(initial_balance=1000, account_type="Savings")

    # Use the Car class
    car.start_engine()  # Output: Checking fuel level... \n Performing ignition sequence... \n Engine started!

    # Use the BankAccount class
    account.deposit(500)  # Output: Checking account balance... \n $500.00 deposited. New balance: $1500.00
    account.withdraw(200) # Output: Checking account balance... \n $200.00 withdrawn. New balance: $1300.00

Classes:
    - Car: A class representing a car with methods to start the engine.
    - BankAccount: A class representing a bank account with methods to deposit and withdraw money.

Public Methods (Car):
    - start_engine(): Starts the car's engine.

Public Methods (BankAccount):
    - deposit(amount): Deposits money into the account.
    - withdraw(amount): Withdraws money from the account.

Optional Arguments for Car:
    - fuel_type (str, optional): The fuel type of the car. Default is "Petrol".

Optional Arguments for BankAccount:
    - initial_balance (float, optional): The initial balance of the account. Default is 0.
    - account_type (str, optional): The type of the bank account (e.g., Savings, Checking). Default is "Savings".

This module provides convenient classes for simulating a car and managing a bank account, offering simple and reusable functionality for various Python projects.
"""

class Car:
    """
    A class representing a car.

    Public Methods:
        start_engine(): Starts the car's engine.

    Private Methods:
        _check_fuel_level(): Checks the fuel level before starting the engine.
        _ignition_sequence(): Performs the ignition sequence.
    """

    def __init__(self, make, model, year, fuel_type="Petrol"):
        """
        Initialize the car.

        Parameters:
            make (str): The make of the car (e.g., Toyota, Honda, etc.).
            model (str): The model of the car (e.g., Camry, Civic, etc.).
            year (int): The manufacturing year of the car.
            fuel_type (str, optional): The fuel type of the car. Default is "Petrol".
        """
        self.make = make
        self.model = model
        self.year = year
        self.fuel_type = fuel_type

    def start_engine(self):
        """Starts the car's engine."""
        self._check_fuel_level()
        self._ignition_sequence()
        print("Engine started!")

    def _check_fuel_level(self):
        """Checks the fuel level before starting the engine."""
        print("Checking fuel level...")

    def _ignition_sequence(self):
        """Performs the ignition sequence."""
        print("Performing ignition sequence...")
