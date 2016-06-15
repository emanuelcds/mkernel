from shamrock.exceptions import InvalidBetException


class SlotPrizeDecomposer(object):
    """
    Decomposes a whole prize to various slot
    machine reel prizes.
    """

    def __init__(self, paytable):
        """
        Initializes slot machine engine.
        @param paytable Paytable class instance.
        """
        self.paytable = paytable

    def decompose(self, bet, multiplier):
        # validate bet level
        if not bet or bet < 0:
            raise InvalidBetException("Invalid Bet: {}".format(bet))

        # get list of possible outcome prizes
        values = list(self.paytable.get_prizes_values())
        # sort it descending for decomposition
        values.sort(reverse=True)
        # iterate over prizes until multiplier is depleted
        prizes = []
        for value in values:
            # if value is contained in multiplier
            if value <= multiplier:
                # create a prize to be associated to a line
                prize = {
                    "pattern": self.paytable.get_prize(value),
                    "won": value * bet
                }
                # append prize to list
                prizes.append(prize)
                # decrement multiplier
                multiplier -= value
        return {
            "prizes": prizes,
            "exceeded": multiplier
        }
