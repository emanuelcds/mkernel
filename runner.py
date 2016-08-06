import requests
import time

req = requests.get("http://localhost:5000/credits")

if req.status_code != requests.codes.ok:
    print("Error({}): {}".format(req.status_code, req.content))

credits = req.json().get("credits")
print(credits)

while credits > 0:
    # play
    bet = 0.25
    r = requests.get("http://localhost:5000/slot/play/1000/{}".format(bet))
    if r.status_code != requests.codes.created:
        raise Exception("Error({}): {}".format(r.status_code, r.content))
    outcome = r.json()
    print(outcome)
    print(outcome.get("credits_before"))
    print(outcome.get("credits_after"))
    before = outcome.get("credits_before")
    credits = outcome.get("credits_after")
    bonus = outcome.get("bonus", [])
    freespins = outcome.get("freespins", [])
    payout = outcome.get("total_win")

    if len(freespins) > 0:
        if credits != before - bet + payout:
            raise Exception("Invalid credits {}, should be {}".format(
                credits,
                (before - bet + payout)
            ))
        time.sleep(60)

    if len(bonus) > 0:
        total_bonus = sum(bonus)
        if credits != before - bet + payout:
            raise Exception("Invalid credits {}, should be {}".format(
                credits,
                (before - bet + payout)
            ))
