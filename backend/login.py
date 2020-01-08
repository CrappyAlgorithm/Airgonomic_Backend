import functools
import json
import flask as fl
from backend.db import get_db

bp = fl.Blueprint('login', __name__, url_prefix='/login')

@bp.route('/',methods=['POST'])
def login():
    if fl.request.method == 'POST':
        username = fl.request.args.get('username', '')
        password = fl.request.args.get('password', '')
        db = get_db()
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        user = db.execute(
            'SELECT id, password FROM user WHERE username = ?', (username,)
        ).fetchone()
        if user is None:
            error = 'User {} is not registered.'.format(username)
        
        if password != user[1]:
            print(password)
            print(user[1])
            error = "Password doesn't match"

        if error is None:
            #replace generate and set token, to use real auth token
            ret = {}
            ret['token'] = user[0]
            return json.dumps(ret)
        return error