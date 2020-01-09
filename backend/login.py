import functools
import json
from flask import (Blueprint, Response, request)
from backend.util import response_code as rc
from backend.util.db import get_db

bp = Blueprint('login', __name__, url_prefix='/login')

@bp.route('/',methods=['GET'])
def login():
    if request.method == 'GET':
        username = request.args.get('username', '')
        password = request.args.get('password', '')
        db = get_db()

        if not username:
            return Response('Username is required', status=rc.PRECONDITION_FAILED)
        if not password:
            return Response('Password is required', status=rc.PRECONDITION_FAILED)
        user = db.execute(
            'SELECT id, password FROM user WHERE username = ?', (username,)
        ).fetchone()
        if user is None:
            return Response('User {} is not registered.'.format(username), status=rc.NOT_FOUND)

        if password != user[1]:
            return Response('Password is wrong.', status=rc.FORBIDDEN)

        #replace generate and set token, to use real auth token
        ret = {}
        ret['token'] = user[0]
        return Response(json.dumps(ret), status=rc.OK, mimetype='application/json')
