import os
import sys

from bottle import run
from bottle import request, response
from bottle import get, post

from shamrock.runtime import SlotRuntime
from shamrock.backend import ShamrockSweepsBackend



BASE_DIR = os.path.dirname(sys.argv[0])
SETTINGS_FILE = os.path.join(BASE_DIR, "settings.json")

Runtime = SlotRuntime(SETTINGS_FILE, ShamrockSweepsBackend)

@post('/slot/play')
def slot_play():
    try:
        body = request.json
    except:
        response.status = 400
        return "Invalid JSON data!"

    if "bet" not in body.keys():
        response.status = 400
        return "Bad Request - Missing 'bet' attribute."
    if "game" not in body.keys():
        response.status = 400
        return "Bad Request - Missing 'game' attribute."

    result = Runtime.handle(str(body.get("game")), float(body.get("bet")))
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


run(host='127.0.0.1', port=int(os.getenv('PORT', 5000)))
