import functools
import json
from flask import (Blueprint, Response, request)
from . import response_code as rc
from backend.db import get_db

bp = Blueprint('configuration', __name__, url_prefix='/configuration')

@bp.route('/',methods=['GET'])
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
