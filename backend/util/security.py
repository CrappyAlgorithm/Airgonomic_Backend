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
    return user_id

def check_admin(token):
    db = get_db()
    user_id = get_user(token)
    if db.execute(
        'SELECT id FROM user WHERE id = ? AND is_admin = 1', (user_id,)
    ).fetchone() is None:
        abort(FORBIDDEN)
    return user_id

def check_user_room(token, room_id):
    db = get_db()
    user_id = get_user(token)
    if db.execute(
        'SELECT id FROM user WHERE id = ? AND is_admin = 1', (user_id,)
    ).fetchone() is None:
        if db.execute(
            'SELECT room.id ' +
            'FROM room join assignment ' +
            'ON room.id = assignment.room_id ' +
            'WHERE assignment.user_id = ? ' +
            'AND assignment.allowed = 1',
            (user_id,)
        ).fetchone() is None:
            abort(400)
    return user_id

def check_user_window(token, window_id):
    db = get_db()
    room_id = db.execute(
        'SELECT room.id ' +
        'FROM room join window ' +
        'ON room.id = window.room_id ' +
        'WHERE window.id = ?',
        (window_id,)
    ).fetchone()
    return check_user_room(token, room_id)

def get_room(token):
    db = get_db()
    if token is None:
        abort(UNAUTHORIZED)
    id = parse(token, 0, min=0)
    if db.execute(
        'SELECT id FROM room WHERE id = ?', (id,)
    ).fetchone() is None:
        abort(BAD_REQUEST)
    return id