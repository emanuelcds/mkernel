import os
from shamrock.runtime import SlotRuntime

config = os.path.join(os.path.dirname(__file__), "settings.json")

runtime = SlotRuntime(config)

runtime.cash_in(1000)
while(runtime.backend.credits):
    print(runtime.handle("1000", .25))
    print(runtime.backend.credits)
