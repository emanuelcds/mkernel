import pymssql
import json


credits = 100.0
spins = 1000000

conn = pymssql.connect("localhost", "no_chance_user", "I want Candy !", "Standalone")

c = conn.cursor()

play_query = """
DECLARE @return_value int;
EXEC @return_value = [dbo].[play_game]
  @gameName = N'KittyKash25',
  @playAmount = .25
SELECT 'multiplier' = @return_value;
"""

credits_query = "SELECT current_balance FROM device_balance"

print("Initializing runner with {0:.2f} credits.".format(credits))
c.execute("UPDATE device_balance SET current_balance = %.2f" % (credits));
conn.commit()

print("Running {} spins...".format(spins))

odds = {}
while spins > 0:
    c.execute(play_query)
    result = c.fetchone()
    won = str(result[0])

    if won not in odds.keys():
        odds[won] = 0
    odds[won] += 1
    spins -= 1

    if spins % 100 == 0:
        print("{} spins left...".format(spins))

    c.execute(credits_query)
    if c.fetchone()[0] < 0.25:
        c.execute("UPDATE device_balance SET current_balance = %.2f" % (credits));
        conn.commit()

print("Game Odds: ", json.dumps(odds))
print("Total of {} possible prizes.".format(len(odds.keys())))
