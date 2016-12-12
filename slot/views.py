import simplejson as json
from decimal import Decimal

from django.views.decorators.http import require_GET
from django.views.decorators.cache import never_cache
from django.http import HttpResponse
from django.conf import settings

from slot.runtime import SlotRuntime
from slot.backend import SlotVLTBackend


def get(func):
    pass

Runtime = SlotRuntime(settings.SLOT_SETTINGS_FILE, SlotVLTBackend)


def serialize(obj):
    return json.dumps(obj, use_decimal=True)


def build_response(obj, code=200):
    msg = serialize(obj)
    return HttpResponse(msg, status=code, content_type='application/json')


@require_GET
@never_cache
def slot_play(req, game, bet, token):
    result = Runtime.handle(str(game), Decimal(bet))
    return build_response(result)


@require_GET
@never_cache
def slot_last_response(req, token):
    return build_response(Runtime.last_result)


@require_GET
@never_cache
def slot_view_prize(req, game, bet, token):
    result = Runtime.pre_review(int(game), Decimal(bet))
    return build_response(result)


@require_GET
@never_cache
def get_credits(req, token):
    credits = Runtime.backend.get_credits()
    result = {
        "credits": credits
    }
    return build_response(result)


@require_GET
@never_cache
def login(req, pin):
    return build_response({
        "token": "0123456789abcdef"
    })


@require_GET
@never_cache
def cashout(req, token):
    return get_credits(req, token)
