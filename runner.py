import requests
from decimal import Decimal

req = requests.get("http://localhost:5000/account/shanvers-token-here")

if req.status_code != requests.codes.ok:
    print("Error({}): {}".format(req.status_code, req.content))

credits = req.json().get("credits")
print(credits)

while credits > 0:
    # play
    bet = Decimal(1)
    r = requests.get(
        "http://localhost:5000/slot/play/1000/{}/token-here".format(
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
    print(outcome)
    if len(freespins) > 0:
        for spin in freespins:
            print(spin.get("total_win"))

    if len(bonus) > 0:
        total_bonus = Decimal(sum(bonus))
        print("BONUS: {0:.2f}".format(total_bonus))

    expected = Decimal((before - bet) + payout)

    if credits != expected:
        print("Before: ", before)
        print("Bet: ", bet)
        print("Payout: ", payout)
        print("Current: ", credits)
        print("Expected: ", expected)
        raise Exception("Invalid credits {}, should be {}".format(
            credits,
            Decimal(before - bet + payout)
        ))
