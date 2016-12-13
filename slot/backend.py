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
        if int(game) in [1000, 1010]:
            self.cache = amount * Decimal("{0:.2f}".format(
                random.choice(
                    [
                        77665 * [Decimal(0.00)],
                        1334 * [Decimal(0.20)],
                        1333 * [Decimal(0.40)],
                        3333 * [Decimal(0.60)],
                        1332 * [Decimal(0.80)],
                        1333 * [Decimal(1.00)],
                        1333 * [Decimal(1.20)],
                        1333 * [Decimal(1.40)],
                        1333 * [Decimal(1.60)],
                        1333 * [Decimal(1.80)],
                        1333 * [Decimal(2.00)],
                        666 * [Decimal(2.20)],
                        666 * [Decimal(2.40)],
                        666 * [Decimal(2.60)],
                        666 * [Decimal(3.00)],
                        666 * [Decimal(4.00)],
                        167 * [Decimal(4.20)],
                        166 * [Decimal(4.80)],
                        166 * [Decimal(5.00)],
                        166 * [Decimal(6.00)],
                        166 * [Decimal(6.60)],
                        166 * [Decimal(7.80)],
                        833 * [Decimal(8.00)],
                        134 * [Decimal(9.00)],
                        133 * [Decimal(10.00)],
                        83 * [Decimal(11.00)],
                        133 * [Decimal(12.00)],
                        83 * [Decimal(13.00)],
                        133 * [Decimal(15.00)],
                        133 * [Decimal(16.00)],
                        325 * [Decimal(20.00)],
                        150 * [Decimal(21.00)],
                        33 * [Decimal(24.00)],
                        32 * [Decimal(27.00)],
                        65 * [Decimal(30.00)],
                        33 * [Decimal(32.00)],
                        33 * [Decimal(33.00)],
                        33 * [Decimal(36.00)],
                        36 * [Decimal(40.00)],
                        33 * [Decimal(42.00)],
                        17 * [Decimal(48.00)],
                        20 * [Decimal(50.00)],
                        16 * [Decimal(52.00)],
                        16 * [Decimal(56.00)],
                        18 * [Decimal(60.00)],
                        10 * [Decimal(66.00)],
                        10 * [Decimal(72.00)],
                        10 * [Decimal(75.00)],
                        10 * [Decimal(81.00)],
                        10 * [Decimal(84.00)],
                        9 * [Decimal(90.00)],
                        8 * [Decimal(96.00)],
                        8 * [Decimal(99.00)],
                        8 * [Decimal(104.00)],
                        8 * [Decimal(105.00)],
                        4 * [Decimal(108.00)],
                        4 * [Decimal(112.00)],
                        4 * [Decimal(120.00)],
                        4 * [Decimal(132.00)],
                        4 * [Decimal(135.00)],
                        5 * [Decimal(144.00)],
                        5 * [Decimal(150.00)],
                        3 * [Decimal(156.00)],
                        3 * [Decimal(165.00)],
                        3 * [Decimal(168.00)],
                        3 * [Decimal(192.00)],
                        3 * [Decimal(208.00)],
                        2 * [Decimal(224.00)],
                        2 * [Decimal(225.00)],
                        2 * [Decimal(240.00)],
                        2 * [Decimal(260.00)],
                        2 * [Decimal(280.00)],
                        2 * [Decimal(300.00)],
                        2 * [Decimal(375.00)],
                        1 * [Decimal(500.00)],
                        1 * [Decimal(800.00)],
                        1 * [Decimal(1000.00)],
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
