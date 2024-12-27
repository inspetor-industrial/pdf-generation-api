from typing import TypeVar
from copy import deepcopy

TCopy: TypeVar = TypeVar("TCopy")


def copy_var(var: TCopy) -> TCopy:
    return deepcopy(var)
