## @package backend.util.arg_parser
#  @author Sebastian Steinmeyer
#  Offers the functinallity to simple parse integer and float within defined range.
from typing import TypeVar
from flask import abort
from backend.util.response_code import *

## A generic typedef for int and float.
T = TypeVar('T', int, float)

## Cast the given value into the type of var val_type.
#  Supports to cast into integer and float.
#  If the value is not castable or not in defined range an error response with code 400 will be thrown.
#  @param value the value to cast
#  @param val_type one representation of the target type(integer or float).
#  @param min the minimal expected value, default is None
#  @param max the maximal expected value, default is None
#  @return the casted value
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
