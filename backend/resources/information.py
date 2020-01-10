import functools
import json
from flask import (Blueprint, Response, request)
from backend.util import response_code as rc
from backend.util.db import get_db
from backend.util.security import get_user

bp = Blueprint('information', __name__, url_prefix='/information')

@bp.route('/',methods=['GET'])
def information():
    db = get_db()
    if request.method == 'GET':
        user_id = get_user(request.args.get('token', None))
        return Response(generate_view(db, user_id), status=rc.OK, mimetype='application/json')

def generate_view(db, user_id):
    cursor = db.cursor()
    ret = {}
    ret['rooms'] = []
    for cur in cursor.execute(
        'SELECT room.id, assignment.alias, assignment.allowed, room.automatic_enable, room.co2, room.humidity, room.is_open ' +
        'FROM room JOIN assignment ' +
        'ON room.id = assignment.room_id ' +
        'WHERE assignment.user_id = ?',
        (user_id,)
    ):
        room_id = cur[0]
        room = {}
        room['room_id'] = cur[0]
        room['alias'] = cur[1]
        room['allowed'] = cur[2]
        room['automati_enable'] = cur[3]
        room['co2'] = cur[4]
        room['humidity'] = cur[5]
        room['is_open'] = cur[6]
        room['windows'] = []

        for cur_w in cursor.execute(
            'SELECT window.id, assignment.alias, window.automatic_enable, window.is_open ' +
            'FROM window join assignment ' +
            'ON window.id = assignment.window_id ' +
            'WHERE window.room_id = ? ' +
            'AND assignment.user_id = ?',
            (room_id, user_id)
        ):
            window = {}
            window['window_id'] = cur_w[0]
            window['alias'] = cur_w[1]
            window['automatic_enable'] = cur_w[2]
            window['is_open'] = cur_w[3]
            room['windows'].append(window)
        ret['rooms'].append(room)
    return json.dumps(ret)