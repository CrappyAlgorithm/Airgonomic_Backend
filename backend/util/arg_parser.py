from typing import TypeVar
from flask import abort
from backend.util.response_code import *

T = TypeVar('T', int, float)

def parse(value, val_type : T, min: T=None, max: T=None):
    if value is None:
        return None
    val = None
    try:
        val = type(val_type)(value)
    except ValueError:
        abort(BAD_REQUEST)

    if min is not None:
        if val < min:
            abort(BAD_REQUEST)
    if max is not None:
        if val > max:
            abort(BAD_REQUEST)
    return val
