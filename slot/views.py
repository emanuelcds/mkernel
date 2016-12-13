import simplejson as json
from decimal import Decimal

from django.views.decorators.http import require_GET
from django.views.decorators.cache import never_cache
from django.http import HttpResponse
from django.conf import settings

from slot.runtime import SlotRuntime
from slot.backend import SlotVLTBackend

from account.models import SessionToken
from account.models import Pin


Runtime = SlotRuntime(settings.SLOT_SETTINGS_FILE, SlotVLTBackend)


def serialize(obj):
    return json.dumps(obj, use_decimal=True)


def build_response(obj, code=200):
    msg = serialize(obj)
    return HttpResponse(msg, status=code, content_type='application/json')


@require_GET
@never_cache
def slot_play(req, game, bet, token):
    result = Runtime.handle(str(game), Decimal(bet), token)
    if not result:
        return build_response({"error": "No credits available!"}, 400)
    return build_response(result)


@require_GET
@never_cache
def slot_last_response(req, token):
    return build_response(Runtime.backend.last_result(token))


@require_GET
@never_cache
def slot_view_prize(req, game, bet, token):
    result = Runtime.pre_review(int(game), Decimal(bet), token)
    return build_response(result)


@require_GET
@never_cache
def get_credits(req, token):
    credits = Runtime.backend.get_credits(token)
    if not credits:
        return build_response({
            "error": "Invalid token!"
        }, 404)
    result = {
        "credits": credits
    }
    return build_response(result)


@require_GET
@never_cache
def login(req, pin):
    try:
        pin = Pin.objects.get(pk=pin)
        if pin.status not in ["active", "new"]:
            return build_response({
                "error": "Pin number cannot be used."
            }, 403)
        pin.status = "active"
        pin.save()
    except:
        return build_response({
            "error": "Invalid PIN Number!"
        }, 404)
    SessionToken.objects.filter(pin=pin).delete()
    token = SessionToken(pin=pin)
    token.save()
    return build_response({
        "token": token.value
    })


@require_GET
@never_cache
def cashout(req, token):
    try:
        session = SessionToken.objects.select_related(
            'pin'
        ).get(value__exact=token)
    except:
        return build_response({
            "error": "Invalid token!"
        }, 404)
    if session.pin:
        if session.pin.status is not "active":
            return build_response({
                "error": "Cannot cashout inactive PIN!"
            })
        session.pin.status = "cashout"
        session.pin.save()
        session.delete()
    return get_credits(req, token)
