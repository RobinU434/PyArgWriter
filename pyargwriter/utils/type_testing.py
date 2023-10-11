from typing import Iterable, Type


def type_of_all(it: Iterable, t: Type) -> bool:
    """Check if all elements in an iterable are of a specific type.

    This function iterates through the elements of an iterable and checks if each element
    is an instance of the specified type 't'.

    Args:
        it (Iterable): An iterable containing elements to be checked.
        t (Type): The type to check each element against.

    Returns:
        bool: True if all elements in the iterable are of the specified type 't', False otherwise.
    """
    for ele in it:
        if not isinstance(ele, t):
            return False
    return True
