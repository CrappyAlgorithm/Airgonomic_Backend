import functools
import json
from flask import (Blueprint, Response, request)
from . import response_code as rc
from backend.db import get_db

bp = Blueprint('configuration', __name__, url_prefix='/configuration')

@bp.route('/',methods=['GET', 'PUT'])
def configuration():
    token = request.args.get('token', '')
    db = get_db()
    if not token:
        return Response('Authentification token is required', status=rc.PRECONDITION_FAILED)
    #need to be changed for token use
    user_id = int(token)
    if db.execute(
        'SELECT id FROM user WHERE id = ? AND is_admin = 1', (user_id,)
    ).fetchone() is None:
        return Response('Not authorized', status=rc.UNAUTHORIZED)

    if request.method == 'GET':
        return Response(generate_view(db), status=rc.OK, mimetype='application/json')

    if request.method == 'PUT':
        try:
            co2 = int(request.args.get('co2', -1))
            humidity = float(request.args.get('humidity', -1.0))
            automatic_enable = int(request.args.get('automatic_enable', -1))
        except ValueError:
            return Response('Error while parsing parameter.', status=rc.BAD_REQUEST)
        set_configuration(db, co2, huidity, automatic_enable)
        return Response('', status=rc.OK)

def generate_view(db):
    cursor = db.cursor()
    ret = {}
    for cur in cursor.execute(
        'SELECT co2, humidity, autoatic_enable FROM configuration'
    ):
        ret['co2'] = cur[0]
        ret['humidity'] = cur[1]
        ret['automatic_enable'] = cur[2]
    return json.dumps(ret)

def set_configuration(db, co2, humidity, automatic_enable):
    if co2 > 0:
        db.execute(
            'UPDATE configuration SET co2 = ? ' +
            'WHERE id = 1',
            (co2,)
        )
    if humidity > 0.0:
        db.execute(
            'UPDATE configuration SET humidity = ? ' +
            'WHERE id = 1',
            (humidity,)
        )
    if automatic_enable >= 0 and automatic_enable < 2:
        db.execute(
            'UPDATE configuration SET automatic_enable = ? ' +
            'WHERE id = 1',
            (automatic_enable,)
        )
    db.commit()