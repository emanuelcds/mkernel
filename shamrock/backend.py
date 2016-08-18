import pymssql
from decimal import Decimal


class ShamrockSweepsBackend(object):
    def __init__(self, options):
        db_opts = ['user', 'password', 'database', 'host']
        for opt in db_opts:
            if opt not in options.keys():
                raise Exception("{} not found in db settings!".format(opt))
        self.options = options
        conn = pymssql.connect(options["host"],
                               options["user"],
                               options["password"],
                               options["database"])
        self.conn = conn
        self.cursor = conn.cursor()

    def play(self, amount, game):
        query = """
        DECLARE @return_value int;
        EXEC @return_value = [dbo].[play_game]
            @gameName = '{}',
            @playAmount = {}
        SELECT 'multiplier' = @return_value;
        """.format(game, amount)

        self.cursor.execute(query)

        result = self.cursor.fetchone()
        won = result[0]
        print("WON: {}".format(float(won)))

        self.conn.commit()
        multiplier = float("%.2f" % (float(won)))
        return multiplier

    def pre_reveal(self, amount, game):
        query = """
        DECLARE @return_value int

        EXEC @return_value = [dbo].[preview_next_prize]
        @gameName = '{}',
        @playAmount = {},
        @offset = 0,
        @numberOfPrizesToRetrieve = 1

        SELECT 'Return Value' = @return_value
        """.format(game, amount)

        self.cursor.execute(query)

        result = self.cursor.fetchone()
        prize = result[1] * Decimal(amount)

        self.conn.commit()
        normalized = float("%.2f" % (float(prize)))
        return normalized

    def get_credits(self):
        query = """
        SELECT current_balance FROM device_balance
        """

        self.cursor.execute(query)

        result = self.cursor.fetchone()
        credits = result[0]
        print("CREDITS: {}".format(credits))
        self.conn.commit()

        return float("%.2f" % (float(credits)))
