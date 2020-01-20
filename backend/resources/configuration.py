import functools
import json
from flask import (Blueprint, Response, request)
from backend.util.response_code import *
from backend.util.db import get_db
from backend.util.arg_parser import parse
from backend.util.security import check_admin, get_room

bp = Blueprint('configuration', __name__, url_prefix='/configuration')

@bp.route('',methods=['GET', 'PUT'])
def configuration():
    db = get_db()
    check_admin(request.args.get('token', None))

    if request.method == 'GET':
        return Response(generate_view(db), status=OK, mimetype='application/json')

    if request.method == 'PUT':
        data = request.get_json()
        if not data:
            return Response('No valid json was send.', status=BAD_REQUEST)
        co2 = parse(data.get('co2', None), 0, min=0)
        humidity = parse(data.get('humidity', None), 0.0, min=0, max=100)
        automatic_enable = parse(data.get('automatic_enable', None), 0, min=0, max=1)
        set_configuration(db, co2, humidity, automatic_enable)
        return Response('', status=OK)

@bp.route('/control',methods=['GET'])
def configuration_control():
    db = get_db()
    get_room(request.args.get('token', None))

    if request.method == 'GET':
        return Response(generate_view(db), status=OK, mimetype='application/json')

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