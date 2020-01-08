import functools
import json
from flask import (Blueprint, Response, request)
from . import response_code as rc
from backend.db import get_db

bp = Blueprint('user', __name__, url_prefix='/user')

@bp.route('/',methods=['GET', 'POST'])
def information():
    if request.method == 'GET':
        token = request.args.get('token', '')
        db = get_db()

        if not token:
            return Response('Authentification token is required', status=rc.PRECONDITION_FAILED)
        #need to be changed for token use
        user_id = int(token)
        if db.execute(
            'SELECT id FROM user WHERE id = ?', (user_id,)
        ).fetchone() is None:
            return Response('Not authorized', status=rc.UNAUTHORIZED)
        return Response(generate_view(db), status=rc.OK, mimetype='application/json')

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