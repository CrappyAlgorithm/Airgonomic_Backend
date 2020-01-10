import functools
import json
from flask import (Blueprint, Response, request)
from backend.util.response_code import *
from backend.util.db import get_db
from backend.util.arg_parser import parse
from backend.util.security import check_user_room, get_user

bp = Blueprint('room', __name__, url_prefix='/room')

@bp.route('/',methods=['PUT'])
def room():
    db = get_db()

    if request.method == 'PUT':
        user_id = None
        room_id = parse(request.args.get('id', None), 0, min=1)
        alias = request.args.get('alias', None)
        is_open = parse(request.args.get('is_open', None), 0, min=0, max=1)
        automatic_enable = parse(request.args.get('automatic_enable', None), 0, min=0, max=1)
        if db.execute(
            'SELECT id FROM room WHERE id = ?', (room_id,)
        ).fetchone() is None:
            return Response('No valid room id given', status=BAD_REQUEST)
        if is_open is not None or automatic_enable is not None:
            user_id = check_user_room(request.args.get('token', None), room_id)
        else:
            user_id = get_user(request.args.get('token', None))
        set_values(db, user_id, room_id, alias, is_open, automatic_enable)
        return Response('', status=OK)

def set_values(db, user_id, room_id, alias, is_open, automatic_enable):
    if alias is not None:
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
    db.commit()