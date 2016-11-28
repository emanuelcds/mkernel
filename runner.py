import requests
from decimal import Decimal, getcontext

getcontext().prec = 2

req = requests.get("http://localhost:5000/credits")

if req.status_code != requests.codes.ok:
    print("Error({}): {}".format(req.status_code, req.content))

credits = req.json().get("credits")
print(credits)

while credits > 0:
    # play
    bet = Decimal(0.25)
    r = requests.get(
        "http://localhost:5000/slot/play/1000/{}".format(
            bet
            )
        )
    if r.status_code != requests.codes.created:
        raise Exception("Error({}): {}".format(r.status_code, r.content))
    outcome = r.json()
    print(outcome)
    print(outcome.get("credits_before"))
    print(outcome.get("credits_after"))
    before = Decimal(outcome.get("credits_before"))
    credits = Decimal(outcome.get("credits_after"))
    bonus = outcome.get("bonus", [])
    freespins = outcome.get("freespins", [])
    payout = Decimal(outcome.get("total_win"))

    if len(freespins) > 0:
        for spin in freespins:
            print(spin.get("total_win"))

    if len(bonus) > 0:
        total_bonus = Decimal(sum(bonus))
        print("BONUS: {0:.2f}".format(total_bonus))

    expected = Decimal(before - bet + payout)

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
