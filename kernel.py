import os
import simplejson as json
from decimal import Decimal

from bottle import run
from bottle import response
from bottle import get
from bottle import default_app

from marimba.runtime import SlotRuntime
from marimba.backend import MarimbaVLTBackend


BASE_DIR = os.path.dirname(os.path.realpath(__file__))
SETTINGS_FILE = os.path.join(BASE_DIR, "settings.json")

Runtime = SlotRuntime(SETTINGS_FILE, MarimbaVLTBackend)


def serialize(obj):
    return json.dumps(obj, use_decimal=True)


def build_response(obj):
    response.status = 200
    response.headers['Content-Type'] = 'application/json'
    msg = serialize(obj)
    response.headers['Content-Length'] = len(msg)
    return msg


@get('/slot/play/<game>/<bet>')
def slot_play(game, bet):
    result = Runtime.handle(str(game), Decimal(bet))
    return build_response(result)


@get('/slot/last_result/')
def slot_last_response():
    return build_response(Runtime.last_result)


@get('/slot/view/<game>/<bet>')
def slot_view_prize(game, bet):
    result = Runtime.pre_review(str(game), Decimal(bet))
    return build_response(result)


@get('/credits')
def get_credits():
    credits = Runtime.backend.get_credits()
    result = {
        "credits": credits
    }
    return build_response(result)

app = default_app()

if __name__ == "__main__":
    run(host='0.0.0.0',
        debug=True,
        server='gunicorn',
        port=int(os.getenv('PORT', 5000)))
