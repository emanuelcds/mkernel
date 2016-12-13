import requests
from decimal import Decimal

req = requests.get("http://localhost:5000/account/58d4f983f0934a9befcd0cf247df7845")
rounds = 0
win = 0
hits = 0
freespin_rounds = 0
bonus_rounds = 0

if req.status_code != requests.codes.ok:
    print("Error({}): {}".format(req.status_code, req.content))

credits = req.json().get("credits")

while credits > 0:
    # play
    bet = Decimal(1.0)
    r = requests.get(
            "http://localhost:5000/slot/play/1010/{0:.2f}/58d4f983f0934a9befcd0cf247df7845".format(
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
        print("RTP: {0:.2f}%".format(100 * Decimal(win)/(rounds * bet)))
        print("Hit: {0:.2f}%".format(100 * Decimal(hits)/rounds))
        print("Freespin Chance: {0:.2f}%".format(100 * Decimal(freespin_rounds)/rounds))
        print("Bonus Chance: {0:.2f}%".format(100 * Decimal(bonus_rounds)/rounds))
