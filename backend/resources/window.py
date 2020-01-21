## @package backend.resources.window
#  Handles the window ressources.
#  See rest api documentation for further information.
import functools
import json
from flask import (Blueprint, Response, request)
from backend.util.response_code import *
from backend.util.db import get_db
from backend.util.arg_parser import parse
from backend.util.security import check_user_window, get_user, get_room

bp = Blueprint('window', __name__, url_prefix='/window')

## Handles the ressource <base>/window with PUT.
@bp.route('',methods=['PUT'])
def window():
    db = get_db()

    if request.method == 'PUT':
        user_id = None
        data = request.get_json()
        if not data:
            return Response('No valid json was send.', status=BAD_REQUEST)
        window_id = parse(data.get('id', None), 0, min=1)
        alias = data.get('alias', None)
        is_open = parse(data.get('is_open', None), 0, min=0, max=1)
        automatic_enable = parse(data.get('automatic_enable', None), 0, min=0, max=1)
        if db.execute(
            'SELECT id FROM window WHERE id = ?', (window_id,)
        ).fetchone() is None:
            return Response('No valid window id given', status=BAD_REQUEST)
        if is_open is not None or automatic_enable is not None:
            user_id = check_user_window(request.args.get('token', None), window_id)
        else:
            user_id = get_user(request.args.get('token', None))
        set_values(db, window_id, user_id, alias, is_open, automatic_enable)
        return Response('', status=OK)

## Handles the ressource <base>/window/control with GET, PUT and POST.
@bp.route('/control',methods=['GET', 'PUT', 'POST'])
def window_control():
    db = get_db()
    room_id = get_room(request.args.get('token', None))

    if request.method == 'GET':
        data = request.get_json()
        if not data:
            return Response('No valid json was send.', status=BAD_REQUEST)
        window_id = parse(data.get('id', None), 0, min=1)
        return Response(generate_view(db, window_id), status=OK, mimetype='application/json')

    if request.method == 'PUT':
        data = request.get_json()
        if not data:
            return Response('No valid json was send.', status=BAD_REQUEST)
        window_id = parse(data.get('id', None), 0, min=1)
        is_open = parse(data.get('is_open', None), 0, min=0, max=1)
        automatic_enable = parse(data.get('automatic_enable', None), 0, min=0, max=1)
        if db.execute(
            'SELECT id FROM window WHERE id = ? and room_id = ?',
            (window_id, room_id)
        ).fetchone() is None:
            return Response('No valid window id given', status=BAD_REQUEST)
        set_values(db, window_id, is_open=is_open)
        return Response('', status=OK)

    if request.method == 'POST':
        return Response(create_window(db, room_id), status=CREATED, mimetype='application/json')

## Generate the JSON response map.
#  @param db the database
#  @param window_id the window id
#  @return the result map
def generate_view(db, window_id):
    cursor = db.cursor()
    ret = {}
    cur = db.execute(
        'SELECT id, automatic_enable, is_open ' +
        'FROM window ' +
        'WHERE window.id = ? ',
        (window_id,)
    ).fetchone()
    ret['id'] = cur[0]
    ret['automatic_enable'] = cur[1]
    ret['is_open'] = cur[2]
    return json.dumps(ret)

## Set the window values in the database
#  @param db the database
#  @param window_id the window id
#  @param user_id the user id
#  @param alias the window alias for the user
#  @param is_open the window state: 0=close, 1=open
#  @param automatic_enable the automatic value: 0=off, 1=on
def set_values(db, window_id, user_id=None, alias=None, is_open=None, automatic_enable=None):
    if alias is not None and user_id is not None:
        db.execute(
            'UPDATE assignment SET alias = ? ' +
            'WHERE user_id = ? ' +
            'AND window_id = ?',
            (alias, user_id, window_id)
        )
    if is_open is not None:
        db.execute(
            'UPDATE window SET is_open = ? ' +
            'WHERE id = ?',
            (is_open, window_id)
        )
    if automatic_enable is not None:
        db.execute(
            'UPDATE window SET automatic_enable = ? ' +
            'WHERE id = ? ',
            (automatic_enable, window_id)
        )
    db.commit()

## Creates a new window.
#  @param db the database
#  @param room_id the room id which should contain the window
#  @return the id of the created window as integer
def create_window(db, room_id):
    cursor = db.cursor()
    db.execute(
        'INSERT INTO window (room_id, is_open, automatic_enable) ' +
        'VALUES (?,0,0)',
        (room_id,)
    )
    id = db.execute(
        'SELECT max(id) FROM window ' + 
        'WHERE room_id = ?',
        (room_id,)
    ).fetchone()[0]

    for user in cursor.execute('SELECT id FROM user'):
        db.execute(
            'INSERT INTO assignment (alias, user_id, allowed, window_id) VALUES ("",?,0,?)',
            (user[0], id)
        )

    ret = {}
    ret['id'] = id
    db.commit()
    return json.dumps(ret)