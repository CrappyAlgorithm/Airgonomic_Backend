## @package backend.resources.login
#  @author Sebastian Steinmeyer
#  Handles the login ressources.
#  See rest api documentation for further information.
import functools
import json
from flask import (Blueprint, Response, request)
from backend.util.response_code import *
from backend.util.db import get_db

bp = Blueprint('login', __name__, url_prefix='/login')

## Handles the ressource <base>/login with POST.
#  Should be GET but the request api of the android application has a bug
#  and sends all GET with body as POST!
@bp.route('',methods=['POST'])
def login():
    db = get_db()
    if request.method == 'POST':
        data = request.get_json()
        if not data:
            return Response('No valid json was send.', status=BAD_REQUEST)
        username = data.get('username', None)
        password = data.get('password', None)
        if not username:
            return Response('Username is required', status=PRECONDITION_FAILED)
        if not password:
            return Response('Password is required', status=PRECONDITION_FAILED)
        user = db.execute(
            'SELECT id, password FROM user WHERE username = ?', (username,)
        ).fetchone()
        if user is None:
            return Response('User {} is not registered.'.format(username), status=NOT_FOUND)
        if password != user[1]:
            return Response('Password is wrong.', status=FORBIDDEN)

        #replace generate and set token, to use real auth token
        ret = {}
        ret['token'] = user[0]
        return Response(json.dumps(ret), status=OK, mimetype='application/json')
