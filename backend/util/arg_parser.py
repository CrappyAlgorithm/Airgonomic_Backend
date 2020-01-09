from typing import TypeVar
from flask import abort

T = TypeVar('T', int, float)

def parse(value, val_type : T, min: T=None, max: T=None):
    if value is None:
        return None
    val = None
    try:
        val = type(val_type)(value)
    except ValueError:
        abort(400)

    if min is not None:
        if val < min:
            abort(400)
    if max is not None:
        if val > max:
            abort(400)
    return val
