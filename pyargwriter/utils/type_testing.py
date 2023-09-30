

from typing import Iterable, Type


def type_of_all(it: Iterable, t: Type):
    for ele in it:
        if not isinstance(ele, t):
            return False
    return True