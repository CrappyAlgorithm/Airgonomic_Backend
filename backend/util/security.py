from flask import abort
from backend.util.db import get_db
from backend.util.response_code import *
from backend.util.arg_parser import parse

def get_user(token):
    db = get_db()
    if token is None:
        abort(UNAUTHORIZED)
    user_id = parse(token, 0, min=0)
    if db.execute(
        'SELECT id FROM user WHERE id = ?', (user_id,)
    ).fetchone() is None:
        abort(BAD_REQUEST)

def is_admin(token):
    user_id = get_user(token)
    if db.execute(
        'SELECT id FROM user WHERE id = ? AND is_admin = 1', (user_id,)
    ).fetchone() is None:
        abort(FORBIDDEN)
    return user_id