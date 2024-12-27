import inspect

from typing import Any


def get_varname(var: Any) -> str:
    current_frame = inspect.currentframe().f_back.f_locals.items()

    for varname, value_of_var in current_frame:
        if value_of_var is var:
            return varname