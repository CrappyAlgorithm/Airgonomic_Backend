import functools
import json
from flask import (Blueprint, Response, request)
from backend.util import response_code as rc
from backend.util.db import get_db
from backend.util.arg_parser import parse

bp = Blueprint('configuration', __name__, url_prefix='/configuration')

@bp.route('/',methods=['GET', 'PUT'])
def configuration():
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
        co2 = parse(request.args.get('co2', None), 0, min=0)
        humidity = parse(request.args.get('humidity', None), 0.0, min=0, max=100)
        automatic_enable = parse(request.args.get('automatic_enable', None), 0, min=0, max=1)
        set_configuration(db, co2, humidity, automatic_enable)
        return Response('', status=rc.OK)

def generate_view(db):
    cursor = db.cursor()
    ret = {}
    for cur in cursor.execute(
        'SELECT co2, humidity, automatic_enable FROM configuration'
    ):
        ret['co2'] = cur[0]
        ret['humidity'] = cur[1]
        ret['automatic_enable'] = cur[2]
    return json.dumps(ret)

def set_configuration(db, co2, humidity, automatic_enable):
    if co2 is not None:
        db.execute(
            'UPDATE configuration SET co2 = ? ' +
            'WHERE id = 1',
            (co2,)
        )
    if humidity is not None:
        db.execute(
            'UPDATE configuration SET humidity = ? ' +
            'WHERE id = 1',
            (humidity,)
        )
    if automatic_enable is not None:
        db.execute(
            'UPDATE configuration SET automatic_enable = ? ' +
            'WHERE id = 1',
            (automatic_enable,)
        )
    db.commit()