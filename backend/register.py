import functools
import flask as fl
from backend.db import get_db

bp = fl.Blueprint('register', __name__, url_prefix='/register')

@bp.route('/',methods=['POST'])
def register():
    if fl.request.method == 'POST':
        username = fl.request.args.get('username', '')
        password = fl.request.args.get('password', '')
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
            add_user(db, username, password)
            return 'success'
        return error

def add_user(db, username, password):
    cursor = db.cursor()
    db.execute(
        'INSERT INTO user (username, password, is_admin) VALUES (?,?,0)',
        (username, password)
    )
    cursor.execute(
        'SELECT id FROM user WHERE username = ?', (username,)
    )
    user_id = cursor.fetchone()[0] 
    print(user_id)
    for room in cursor.execute('SELECT id FROM room'):
        db.execute(
            'INSERT INTO assignment (alias, user_id, allowed, room_id) VALUES ("",?,0,?)',
            (user_id, room[0])
        )
    for window in cursor.execute('SELECT id FROM window'):
        db.execute(
            'INSERT INTO assignment (alias, user_id, allowed, window_id) VALUES ("",?,0,?)',
            (user_id, window[0])
        )
    db.commit()

