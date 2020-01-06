import functools
import flask as fl
from backend.db import get_db

bp = fl.Blueprint('register', __name__, url_prefix='/register')

@bp.route('/',methods=('POST'))
def register():
    if request.method == 'POST':
        username = request.args.get('username', '')
        password = request.args.get('password', '')
        db = get_db()
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        elif db.execute(
            'SELECT id FROM user WHERE username = ?', (username,)
        ).fetchone() is not None:
            error = 'User {} is already registered.'.format(username)

        if error is None:
            #insert user to db and generate link to all rooms/windows
            #send success
            pass
        #send error