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
        self.pool = {
            1000: 77665 * [0.00] +
                1334 * [0.20] +
                1333 * [0.40] +
                3333 * [0.60] +
                1332 * [0.80] +
                1333 * [1.00] +
                1333 * [1.20] +
                1333 * [1.40] +
                1333 * [1.60] +
                1333 * [1.80] +
                1333 * [2.00] +
                666 * [2.20] +
                666 * [2.40] +
                666 * [2.60] +
                666 * [3.00] +
                666 * [4.00] +
                167 * [4.20] +
                166 * [4.80] +
                166 * [5.00] +
                166 * [6.00] +
                166 * [6.60] +
                166 * [7.80] +
                833 * [8.00] +
                134 * [9.00] +
                133 * [10.00] +
                83 * [11.00] +
                133 * [12.00] +
                83 * [13.00] +
                133 * [15.00] +
                133 * [16.00] +
                325 * [20.00] +
                150 * [21.00] +
                33 * [24.00] +
                32 * [27.00] +
                65 * [30.00] +
                33 * [32.00] +
                33 * [33.00] +
                33 * [36.00] +
                36 * [40.00] +
                33 * [42.00] +
                17 * [48.00] +
                20 * [50.00] +
                16 * [52.00] +
                16 * [56.00] +
                18 * [60.00] +
                10 * [66.00] +
                10 * [72.00] +
                10 * [75.00] +
                10 * [81.00] +
                10 * [84.00] +
                9 * [90.00] +
                8 * [96.00] +
                8 * [99.00] +
                8 * [104.00] +
                8 * [105.00] +
                4 * [108.00] +
                4 * [112.00] +
                4 * [120.00] +
                4 * [132.00] +
                4 * [135.00] +
                5 * [144.00] +
                5 * [150.00] +
                3 * [156.00] +
                3 * [165.00] +
                3 * [168.00] +
                3 * [192.00] +
                3 * [208.00] +
                2 * [224.00] +
                2 * [225.00] +
                2 * [240.00] +
                2 * [260.00] +
                2 * [280.00] +
                2 * [300.00] +
                2 * [375.00] +
                1 * [500.00] +
                1 * [800.00] +
                1 * [1000.00],
        }
        self.pool[1010] = self.pool[1000]

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
        if int(game) in [1000, 1010]:
            self.cache = amount * Decimal("{0:.2f}".format(
                random.choice(self.pool[game])
            ))
            pprint("Fetched Prize: {}".format(self.cache))

    def pre_reveal(self, amount, game):
        if not self.cache:
            self.fetch_prize(amount, game)
        return self.cache

    def get_credits(self):
        return self.credits
