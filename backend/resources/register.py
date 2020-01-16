import functools
from flask import (Blueprint, Response, request)
from backend.util.response_code import *
from backend.util.db import get_db

bp = Blueprint('register', __name__, url_prefix='/register')

@bp.route('',methods=['POST'])
def register():
    db = get_db()
    if request.method == 'POST':
        data = request.get_json()
        if not data:
            return Response('No valid json was send.', status=BAD_REQUEST)
        username = data.get("username", None)
        password = data.get("password", None)
        if not username:
            return Response('Username is required', status=PRECONDITION_FAILED)
        if not password:
            return Response('Password is required', status=PRECONDITION_FAILED)
        if db.execute(
            'SELECT id FROM user WHERE username = ?', (username,)
        ).fetchone() is not None:
            return Response('User {} is already registered.'.format(username), status=CONFLICT)

        add_user(db, username, password)
        return Response('', status=CREATED)

def add_user(db, username, password):
    cursor = db.cursor()
    db.execute(
        'INSERT INTO user (username, password, is_admin) VALUES (?,?,0)',
        (username, password)
    )
    cursor.execute(
        'SELECT id FROM user WHERE username = ?', (username,)
    )
    user_id = cursor.fetchone()[0] 
    print(user_id)
    for room in cursor.execute('SELECT id FROM room'):
        db.execute(
            'INSERT INTO assignment (alias, user_id, allowed, room_id) VALUES ("",?,0,?)',
            (user_id, room[0])
        )
    for window in cursor.execute('SELECT id FROM window'):
        db.execute(
            'INSERT INTO assignment (alias, user_id, allowed, window_id) VALUES ("",?,0,?)',
            (user_id, window[0])
        )
    db.commit()

