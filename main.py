import os
import sys
import time
from shamrock.runtime import SlotRuntime
from shamrock.backend import ShamrockSweepsBackend

config = os.path.join(os.path.dirname(sys.argv[0]), "settings.json")

runtime = SlotRuntime(config, ShamrockSweepsBackend)

#runtime.backend.cashin(10000)

while(runtime.backend.get_credits()):
    bet = 1
    prize = runtime.handle("1000", bet)
    print(prize)
    if prize.get("total_win", 0) > 0:
            print("TOTAL WIN: {}".format(prize.get("total_win")))
            time.sleep(1)
    print(runtime.backend.get_credits())
