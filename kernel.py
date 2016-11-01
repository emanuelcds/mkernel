import os
import simplejson as json

from bottle import run
from bottle import request, response
from bottle import get
from bottle import default_app

from marimba.runtime import SlotRuntime
from marimba.backend import MarimbaVLTBackend


BASE_DIR = os.path.dirname(os.path.realpath(__file__))
SETTINGS_FILE = os.path.join(BASE_DIR, "settings.json")

Runtime = SlotRuntime(SETTINGS_FILE, MarimbaVLTBackend)


@get('/slot/play/<game>/<bet>')
def slot_play(game, bet):
    result = Runtime.handle(str(game), float(bet))
    response.status = 201
    response.headers['Content-Type'] = 'application/json'
    return json.dumps(result)


@get('/slot/view/<game>/<bet>')
def slot_view_prize(game, bet):
    result = Runtime.pre_review(str(game), float(bet))
    response.status = 201
    response.headers['Content-Type'] = 'application/json'
    return json.dumps(result)


@get('/credits')
def get_credits():
    credits = Runtime.backend.get_credits()
    result = {
        "credits": credits
    }
    request.status = 200
    response.headers['Content-Type'] = 'application/json'
    return json.dumps(result)

app = default_app()

if __name__ == "__main__":
    run(host='0.0.0.0',
        port=int(os.getenv('PORT', 5000)),
        server="guncorn")
