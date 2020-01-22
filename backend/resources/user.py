## @package backend.resources.user
#  Handles the user ressources.
#  See rest api documentation for further information.
import functools
import json
from flask import (Blueprint, Response, request)
from backend.util.response_code import *
from backend.util.db import get_db
from backend.util.arg_parser import parse
from backend.util.security import check_admin

bp = Blueprint('user', __name__, url_prefix='/user')

## Handles the ressource <base>/user with GET and PUT.
@bp.route('',methods=['GET', 'PUT'])
def user():
    db = get_db()
    check_admin(request.args.get('token', None))

    if request.method == 'GET':
        return Response(generate_view(db), status=OK, mimetype='application/json')

    if request.method == 'PUT':
        data = request.get_json()
        print(f'JSON: {data}')
        if not data:
            return Response('No valid json was send.', status=BAD_REQUEST)
        user_id = parse(data.get('id', None), 0)
        is_admin = parse(data.get('is_admin', None), 0, min=0, max=1)
        allow_room = parse(data.get('allow_room', None), 0, min=1)
        revoke_room = parse(data.get('revoke_room', None), 0, min=1)
        if db.execute(
            'SELECT id FROM user WHERE id = ?', (user_id,)
        ).fetchone() is None:
            return Response('No valid user id given', status=BAD_REQUEST)
        set_values(db, user_id, is_admin, allow_room, revoke_room)
        return Response('', status=OK)

## Generate the JSON response map.
#  @param db the database
#  @return the result map
def generate_view(db):
    cursor = db.cursor()
    cursor_r = db.cursor()
    ret = {}
    ret['user'] = []
    for cur in cursor.execute(
        'SELECT id, username, is_admin FROM user'
    ):
        user_id = cur[0]
        user = {}
        user['user_id'] = cur[0]
        user['username'] = cur[1]
        user['is_admin'] = cur[2]
        user['rooms'] = []

        for cur_r in cursor_r.execute(
            'SELECT room.id, assignment.allowed ' +
            'FROM room join assignment ' +
            'ON room.id = assignment.room_id ' +
            'WHERE assignment.user_id = ? ',
            (user_id,)
        ):
            room = {}
            room['room_id'] = cur_r[0]
            room['allowed'] = cur_r[1]
            user['rooms'].append(room)
        ret['user'].append(user)
    return json.dumps(ret)

## Set the user values in the database
#  @param db the database
#  @param user_id the user id
#  @param is_admin defines the user rights: 0=no_admin, 1=admin
#  @param allow_room id of the room the user should get rights
#  @param revoke_room id of the room the user should lose rights
def set_values(db, user_id, is_admin, allow_room, revoke_room):
    if is_admin is not None:
        db.execute(
            'UPDATE user SET is_admin = ? ' +
            'WHERE id = ?',
            (is_admin, user_id)
        )
    if allow_room is not None:
        db.execute(
            'UPDATE assignment SET allowed = 1 ' +
            'WHERE user_id = ? ' +
            'AND room_id = ?',
            (user_id, allow_room)
        )
    if revoke_room is not None:
        db.execute(
            'UPDATE assignment SET allowed = 0 ' +
            'WHERE user_id = ? ' +
            'AND room_id = ?',
            (user_id, revoke_room)
        )
    db.commit()