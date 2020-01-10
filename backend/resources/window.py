import functools
import json
from flask import (Blueprint, Response, request)
from backend.util.response_code import *
from backend.util.db import get_db
from backend.util.arg_parser import parse
from backend.util.security import check_user_window, get_user

bp = Blueprint('window', __name__, url_prefix='/window')

@bp.route('',methods=['PUT'])
def user():
    db = get_db()

    if request.method == 'PUT':
        user_id = None
        window_id = parse(request.args.get('id', None), 0, min=1)
        alias = request.args.get('alias', None)
        is_open = parse(request.args.get('is_open', None), 0, min=0, max=1)
        automatic_enable = parse(request.args.get('automatic_enable', None), 0, min=0, max=1)
        if db.execute(
            'SELECT id FROM window WHERE id = ?', (window_id,)
        ).fetchone() is None:
            return Response('No valid window id given', status=BAD_REQUEST)
        if is_open is not None or automatic_enable is not None:
            user_id = check_user_window(request.args.get('token', None), window_id)
        else:
            user_id = get_user(request.args.get('token', None))
        set_values(db, user_id, window_id, alias, is_open, automatic_enable)
        return Response('', status=OK)

def set_values(db, user_id, window_id, alias, is_open, automatic_enable):
    if alias is not None:
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