import os
import sys

from bottle import run
from bottle import request, response
from bottle import get

from shamrock.runtime import SlotRuntime
from shamrock.backend import ShamrockSweepsBackend


BASE_DIR = os.path.dirname(sys.argv[0])
SETTINGS_FILE = os.path.join(BASE_DIR, "settings.json")

Runtime = SlotRuntime(SETTINGS_FILE, ShamrockSweepsBackend)


@get('/slot/play/<game>/<bet>')
def slot_play(game, bet):
    result = Runtime.handle(str(game), float(bet))
    response.status = 201
    response.headers['Content-Type'] = 'application/json'
    return result


@get('/slot/view/<game>/<bet>')
def slot_view_prize(game, bet):
    result = Runtime.pre_review(str(game), float(bet))
    response.status = 201
    response.headers['Content-Type'] = 'application/json'
    return result


@get('/credits')
def get_credits():
    credits = Runtime.backend.get_credits()
    result = {
        "credits": credits
    }
    request.status = 200
    response.headers['Content-Type'] = 'application/json'
    return result


run(host='0.0.0.0', port=int(os.getenv('PORT', 5000)))
