import os
import simplejson as json
from decimal import Decimal

from bottle import run
from bottle import response
from bottle import get
from bottle import default_app

from slot.runtime import SlotRuntime
from slot.backend import SlotVLTBackend


BASE_DIR = os.path.dirname(os.path.realpath(__file__))
SETTINGS_FILE = os.path.join(BASE_DIR, "slots.json")

Runtime = SlotRuntime(SETTINGS_FILE, SlotVLTBackend)


def serialize(obj):
    return json.dumps(obj, use_decimal=True)


def build_response(obj):
    response.status = 200
    response.headers['Content-Type'] = 'application/json'
    msg = serialize(obj)
    response.headers['Content-Length'] = len(msg)
    return msg


@get('/slot/play/<game>/<bet>/<token>')
def slot_play(game, bet, token):
    result = Runtime.handle(str(game), Decimal(bet))
    return build_response(result)


@get('/slot/last_result/<token>')
def slot_last_response(token):
    return build_response(Runtime.last_result)


@get('/slot/reveal/<game>/<bet>/<token>')
def slot_view_prize(game, bet, token):
    result = Runtime.pre_review(str(game), Decimal(bet))
    return build_response(result)


@get('/account/<token>')
def get_credits(token):
    credits = Runtime.backend.get_credits()
    result = {
        "credits": credits
    }
    return build_response(result)


@get('/account/login/<pin>')
def login(pin):
    return {
        "token": "0123456789abcdef"
    }


@get('/account/cashout/<token>')
def cashout(token):
    return get_credits(token)


app = default_app()

if __name__ == "__main__":
    run(host='0.0.0.0',
        debug=True,
        server='gunicorn',
        port=int(os.getenv('PORT', 5000)))
