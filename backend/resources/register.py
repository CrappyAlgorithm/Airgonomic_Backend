## @package backend.resources.register
#  Handles the register ressources.
#  See rest api documentation for further information.
import functools
from flask import (Blueprint, Response, request)
from backend.util.response_code import *
from backend.util.db import get_db

bp = Blueprint('register', __name__, url_prefix='/register')

## Handles the ressource <base>/register with POST.
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

## Creates a new user with given name and password.
#  @param db the database
#  @param username the name of the user
#  @param password the password of the user
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
    for room in cursor.execute('SELECT id FROM room'):
        db.execute(
            'INSERT INTO assignment (alias, user_id, allowed, room_id) VALUES (?,?,0,?)',
            (f'Raum {room[0]}', user_id, room[0])
        )
    for window in cursor.execute('SELECT id FROM window'):
        db.execute(
            'INSERT INTO assignment (alias, user_id, allowed, window_id) VALUES (?,?,0,?)',
            (f'Fenster {window[0]}', user_id, window[0])
        )
    db.commit()

