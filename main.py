import os
import time
from shamrock.runtime import SlotRuntime

config = os.path.join(os.path.dirname(__file__), "settings.json")

runtime = SlotRuntime(config)

runtime.cash_in(1000)
while(runtime.backend.credits):
    bet = 1
    prize = runtime.handle("1000", bet)
    print(prize)
    if len(prize.get("freespins", [])) > 0:
        print("TOTAL WIN: {}".format(prize.get("total_win")))
        after = prize.get("credits_after")
        before = prize.get("credits_before")
        if prize.get("total_win") != (after - before) + bet:
            print("After: ", after)
            print("Before: ", before)
            print("Result: ", after - before)
            time.sleep(10)
    print(runtime.backend.get_credits())
