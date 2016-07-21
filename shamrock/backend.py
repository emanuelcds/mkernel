import pymssql

class ShamrockSweepsBackend(object):
    def __init__(self, options):
        db_opts = ['user', 'password', 'database', 'host']
        for opt in db_opts:
            if opt not in options.keys():
                raise Exception("{} not found in db settings!".format(opt))
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

        multiplier = float("%.2f" % (float(won)))
        return multiplier

    def get_credits(self):
        query = """
        SELECT current_balance FROM device_balance
        """

        self.cursor.execute(query)

        result = self.cursor.fetchone()
        credits = result[0]

        return float("%.2f" % (float(credits)))
    
    def cashin(self, amount):
        query = """
        UPDATE device_balance SET current_balance = current_balance + {}
        """.format(amount)

        self.cursor.execute(query)
        self.conn.commit()

