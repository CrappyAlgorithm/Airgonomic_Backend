import functools
import json
from flask import (Blueprint, Response, request)
from . import response_code as rc
from backend.db import get_db
from backend.util.arg_parser import parse

bp = Blueprint('user', __name__, url_prefix='/user')

@bp.route('/',methods=['GET', 'PUT'])
def user():
    token = request.args.get('token', '')
    db = get_db()
    if not token:
        return Response('Authentification token is required', status=rc.UNAUTHORIZED)
    #need to be changed for token use
    user_id = int(token)
    if db.execute(
        'SELECT id FROM user WHERE id = ? AND is_admin = 1', (user_id,)
    ).fetchone() is None:
        return Response('Not authorized', status=rc.FORBIDDEN)

    if request.method == 'GET':
        return Response(generate_view(db), status=rc.OK, mimetype='application/json')

    if request.method == 'PUT':
        user_id = parse(request.args.get('id', None), 0)
        is_admin = parse(request.args.get('is_admin', None), 0, min=0, max=1)
        allow_room = parse(request.args.get('allow_room', None), 0, min=0, max=1)
        revoke_room = parse(request.args.get('revoke_room', None), 0, min=0, max=1)
        if db.execute(
            'SELECT id FROM user WHERE id = ?', (user_id,)
        ).fetchone() is None:
            return Response('No valid user id given', status=rc.FORBIDDEN)
        set_values(db, user_id, is_admin, allow_room, revoke_room)
        return Response('', status=rc.OK)

def generate_view(db):
    cursor = db.cursor()
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

        for cur_r in cursor.execute(
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

def set_values(db, user_id, is_admin, allow_room, revoke_room):
    if is_admin >= 0 and is_admin < 2:
        db.execute(
            'UPDATE user SET is_admin = ? ' +
            'WHERE id = ?',
            (is_admin, user_id)
        )
    if allow_room >= 0:
        db.execute(
            'UPDATE assignment SET allowed = 1 ' +
            'WHERE user_id = ? ' +
            'AND room_id = ?',
            (user_id, allow_room)
        )
    if revoke_room >= 0:
        db.execute(
            'UPDATE assignment SET allowed = 0 ' +
            'WHERE user_id = ? ' +
            'AND room_id = ?',
            (user_id, revoke_room)
        )
    db.commit()