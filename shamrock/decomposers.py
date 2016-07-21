from shamrock.exceptions import InvalidBetException
from random import randint
from random import choice
from random import shuffle


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

    def handle(self, bet, multiplier, lines, force_freespin=False):
        """
        Decomposes the prize acoordingly to game
        settings and limitations
        """
        # initialize values
        self.bonus = []
        self.freespins = []
        self.prizes = []

        # get amount of prizes for the given multiplier
        decomposed = self.decompose(bet, multiplier)
        self.prizes = decomposed["prizes"]
        prize_amount = len(decomposed["prizes"])
        # maximum paylines to be a base game prize
        max_paylines = len(lines) // 5

        # bonus flag
        bonus = False

        # triggers bonus in case of unforeseen outcome
        if decomposed["exceeded"] > 1:
            bonus = True
        # tries to trigger freespins if has many prizes
        elif prize_amount > max_paylines or force_freespin:
            feature = choice(["freespin", "bonus"])
            if feature == "freespin" or force_freespin:
                spin_amount = self.paytable.get_freespins(prize_amount)
                # if cannot handle prize amount with freespins, triggers bonus
                if not spin_amount:
                    bonus = True
                else:
                    # triggers freespins
                    self.freespin_prize(decomposed["prizes"])
            # triggers bonus
            else:
                bonus = True

        if bonus:
            self.bonus_prize(multiplier * bet)

        return {
            "prizes": self.prizes,
            "freespins": self.freespins,
            "bonus": self.bonus
        }

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
                    "pattern": self.paytable.get_prize(value).get("pattern"),
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

    def bonus_prize(self, value):
        """
        Decomposes a given value into steps of prizes.
        """
        bonus = self.paytable.get_bonus()
        if not bonus:
            raise Exception("Cannot handle bonus prizes!")
        parts = []
        total = 100
        while total > 0:
            rnd = randint(0, min(25, total))
            total -= rnd
            parts.append(rnd / 100)
        prizes = []
        for i in parts:
            prizes.append(float("%.2f" % (value * i)))
        self.bonus = prizes
        self.prizes = [bonus]

    def freespin_prize(self, prizes):
        """
        Decomposes a given value into series of prizes for spins.
        """
        # determine amount of spins
        freespin = self.paytable.get_freespins(len(prizes))
        if not freespin:
            raise Exception("Cannot handle this amount of spins!")
        # in case of prizes does not match the amount of freespins
        while len(prizes) < freespin["freespins"]:
            empty_prize = {
                "pattern": [],
                "won": 0
            }
            prizes.append(empty_prize)

        # get the decomposed prize list for each element
        shuffle(prizes)
        self.freespins = prizes
        self.prizes = [freespin]
