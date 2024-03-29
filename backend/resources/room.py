## @package backend.resources.room
#  @author Sebastian Steinmeyer
#  Handles the room ressources.
#  See rest api documentation for further information.
import functools
import json
from flask import (Blueprint, Response, request)
from backend.util.response_code import *
from backend.util.db import get_db
from backend.util.arg_parser import parse
from backend.util.security import check_user_room, get_user, get_room

bp = Blueprint('room', __name__, url_prefix='/room')

## Handles the ressource <base>/room with PUT.
@bp.route('',methods=['PUT'])
def room():
    db = get_db()

    if request.method == 'PUT':
        user_id = None        
        data = request.get_json()
        if not data:
            return Response('No valid json was send.', status=BAD_REQUEST)
        room_id = parse(data.get('id', None), 0, min=1)
        alias = data.get('alias', None)
        is_open = parse(data.get('is_open', None), 0, min=0, max=1)
        automatic_enable = parse(data.get('automatic_enable', None), 0, min=0, max=1)
        if db.execute(
            'SELECT id FROM room WHERE id = ?', (room_id,)
        ).fetchone() is None:
            return Response('No valid room id given', status=BAD_REQUEST)
        if is_open is not None or automatic_enable is not None:
            user_id = check_user_room(request.args.get('token', None), room_id)
        else:
            user_id = get_user(request.args.get('token', None))
        set_values(db, room_id, user_id, alias, is_open, automatic_enable)
        return Response('', status=OK)

## Handles the ressource <base>/room/control with GET, PUT and POST.
@bp.route('/control',methods=['GET', 'PUT', 'POST'])
def room_control():
    db = get_db()

    if request.method == 'GET':
        room_id = get_room(request.args.get('token', None))
        return Response(generate_view(db, room_id), status=OK, mimetype='application/json')

    if request.method == 'PUT':
        room_id = get_room(request.args.get('token', None))
        data = request.get_json()
        if not data:
            return Response('No valid json was send.', status=BAD_REQUEST)
        co2 = parse(data.get('co2', None), 0, min=0)
        humidity = parse(data.get('humidity', None), 0.0, min=0)
        is_open = parse(data.get('is_open', None), 0, min=0, max=1)
        set_values(db, room_id, co2=co2, humidity=humidity, is_open=is_open)
        return Response('', status=OK)

    if request.method == 'POST':
        return Response(create_room(db), status=CREATED, mimetype='application/json')

## Set the room values in the database
#  @param db the database
#  @param room_id the room id
#  @param user_id the user id
#  @param alias the room alias for the user
#  @param is_open the room state: 0=close, 1=open
#  @param automatic_enable the automatic value: 0=off, 1=on
#  @param co2 the co2 value as integer
#  @param humidity the humidity value as float
def set_values(db, room_id, user_id=None, alias=None, is_open=None, automatic_enable=None, co2=None, humidity=None):
    if alias is not None and user_id is not None:
        db.execute(
            'UPDATE assignment SET alias = ? ' +
            'WHERE user_id = ? ' +
            'AND room_id = ?',
            (alias, user_id, room_id)
        )
    if is_open is not None:
        db.execute(
            'UPDATE room SET is_open = ? ' +
            'WHERE id = ?',
            (is_open, room_id)
        )
    if automatic_enable is not None:
        db.execute(
            'UPDATE room SET automatic_enable = ? ' +
            'WHERE id = ? ',
            (automatic_enable, room_id)
        )
    if co2 is not None:
        db.execute(
            'UPDATE room SET co2 = ? ' +
            'WHERE id = ?',
            (co2, room_id)
        )
    if humidity is not None:
        db.execute(
            'UPDATE room SET humidity = ? ' +
            'WHERE id = ?',
            (humidity, room_id)
        )
    db.commit()

## Generate the JSON response map.
#  @param db the database
#  @param room_id the room id
#  @return the result map
def generate_view(db, room_id):
    cursor = db.cursor()
    ret = {}
    cur = db.execute(
        'SELECT id, automatic_enable, co2, humidity, is_open ' +
        'FROM room ' +
        'WHERE room.id = ?',
        (room_id,)
    ).fetchone()
    ret['id'] = cur[0]
    ret['automatic_enable'] = cur[1]
    ret['co2'] = cur[2]
    ret['humidity'] = cur[3]
    ret['is_open'] = cur[4]
    return json.dumps(ret)

## Creates a new room.
#  @param db the database
#  @return the id of the created room as integer
def create_room(db):
    cursor = db.cursor()
    db.execute(
        'INSERT INTO room (is_open, automatic_enable, co2, humidity) ' +
        'VALUES (0, 0, 0, 0.0)'
    )
    id = db.execute(
        'SELECT max(id) FROM room'
    ).fetchone()[0]

    for user in cursor.execute('SELECT id FROM user'):
        db.execute(
            'INSERT INTO assignment (alias, user_id, allowed, room_id) VALUES (?,?,0,?)',
            (f'Raum {id}', user[0], id)
        )

    ret = {}
    ret['token'] = id
    db.commit()
    return json.dumps(ret)