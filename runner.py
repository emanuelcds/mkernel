import requests
from decimal import Decimal

req = requests.get("http://mkernel.herokuapp.com/account/98f8911a6c74914c4ce3b19948502560")
rounds = 0
win = 0
hits = 0
anticipations_amnt = 0
freespin_rounds = 0
bonus_rounds = 0

if req.status_code != requests.codes.ok:
    print("Error({}): {}".format(req.status_code, req.content))

credits = req.json().get("credits")

while credits > 0:
    # play
    bet = Decimal(0.25)
    r = requests.get(
            "http://mkernel.herokuapp.com/slot/play/1010/{0:.2f}/98f8911a6c74914c4ce3b19948502560".format(
            bet
            )
        )
    if r.status_code != requests.codes.ok:
        raise Exception("Error({}): {}".format(r.status_code, r.content))
    outcome = r.json()
    before = Decimal("{0:.2f}".format(outcome.get("credits_before")))
    credits = Decimal("{0:.2f}".format(outcome.get("credits_after")))
    bonus = outcome.get("bonus", [])
    freespins = outcome.get("freespins", [])
    anticipations_amnt += len(outcome.get("antecipation", [])) > 0
    payout = Decimal("{0:.2f}".format(outcome.get("total_win")))
    win += payout
    if payout > 0:
        hits += 1
    rounds += 1
    if len(freespins) > 0:
        freespin_rounds += 1

    if len(bonus) > 0:
        bonus_rounds += 1

    expected = Decimal((before - bet) + payout)

    if abs(credits - expected) > 0.05:
        print("Before: ", before)
        print("Bet: ", bet)
        print("Payout: ", payout)
        print("Current: ", credits)
        print("Expected: ", expected)
        raise Exception("Invalid credits {}, should be {}".format(
            credits,
            Decimal(before - bet + payout)
        ))
    else:
        print("Rounds: {}".format(rounds))
        print("Anticipations: {}".format(anticipations_amnt))
        print("RTP: {0:.2f}%".format(100 * Decimal(win)/(rounds * bet)))
        print("Hit: {0:.2f}%".format(100 * Decimal(hits)/rounds))
        print("Freespin Chance: {0:.2f}%".format(100 * Decimal(freespin_rounds)/rounds))
        print("Bonus Chance: {0:.2f}%".format(100 * Decimal(bonus_rounds)/rounds))
