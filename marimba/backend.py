import random
from decimal import Decimal


class MarimbaVLTBackend(object):
    def __init__(self, options):
        """
        Initialize connection with backend database.
        """
        self.cache = Decimal(0)
        self.credits = Decimal(1000)

    def play(self, amount, game):
        amount = Decimal(amount)
        self.credits -= amount
        if not self.cache:
            self.fetch_prize(amount, game)
        prize = self.cache
        self.fetch_prize(amount, game)
        self.credits += prize
        return prize

    def fetch_prize(self, amount, game):
        self.cache = Decimal(
            random.choice(
                [
                    0.2, 0.6, 2.0,
                    0.4, 1.2, 4.0,
                    0.0, 84.0, 14.8,
                    8.0, 0.0, 141,
                ]
            )
        )

    def pre_reveal(self, amount, game):
        if not self.cache:
            self.fetch_prize(amount, game)
        return self.cache

    def get_credits(self):
        return self.credits
