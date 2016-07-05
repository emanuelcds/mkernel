from shamrock.exceptions import InvalidBetException
from random import randint
from random import choice


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
            "exceeded": multiplier * bet
        }

    def decompose_bonus(self, value):
        """
        Decomposes a given value into steps of prizes.
        """
        parts = []
        total = 100
        while total > 0:
            rnd = randint(0, max(25, total))
            total -= rnd
            parts.append(rnd)
        prizes = []
        for i in parts:
            prizes.append(value * i)
        return prizes

    def decompose_spins(self, spins, bet, multiplier):
        """
        Decomposes a given value into series of prizes for spins.
        """
        # get possible range of prize values
        values = list(self.paytable.get_prizes_values())
        prize_list = []

        # iterates over values picking one by one until multiplier get depleted
        while multiplier > 0:
            value = choice(values)
            multiplier -= value
            prize_list.append(value)

        # iterates over prize_list until it get reduced to the amount of spins
        while len(prize_list) > spins:
            pick_a = choice(prize_list)
            prize_list.remove(pick_a)
            pick_b = choice(prize_list)
            prize_list.remove(pick_b)
            prize_list.append(pick_a + pick_b)

        # get the decomposed prize list for each element
        prizes = []
        for prize_value in prize_list:
            prizes.append(self.decompose(bet, prize_value).get("prizes"))
        return prizes
