import random
from decimal import Decimal
from pprint import pprint


class SlotVLTBackend(object):
    def __init__(self, options):
        """
        Initialize connection with backend database.
        """
        self.cache = Decimal(0)
        self.credits = Decimal(1000)

    def play(self, amount, game):
        amount = Decimal(amount)
        pprint("Credits Before: {}".format(self.credits))
        self.credits -= amount
        pprint("Credits After: {}".format(self.credits))
        self.fetch_prize(amount, game)
        prize = self.cache
        self.credits += prize
        pprint("Prize: {}".format(self.cache))
        pprint("Credits After Prize: {}".format(self.credits))
        return prize

    def fetch_prize(self, amount, game):
        self.cache = amount * Decimal("{0:.2f}".format(
            random.choice(
                [
                    0.2, 0.6, 2.0,
                    0.4, 1.2, 4.0,
                    0.0, 84.0, 14.8,
                    8.0, 0.0, 141,
                ]
            )
        ))
        pprint("Fetched Prize: {}".format(self.cache))

    def pre_reveal(self, amount, game):
        if not self.cache:
            self.fetch_prize(amount, game)
        return self.cache

    def get_credits(self):
        return self.credits
