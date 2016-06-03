from unittest import TestCase
from shamrock.paytable import SlotPayTable
from shamrock.exceptions import ExistingCombinationException


class SlotPayTableTest(TestCase):
    """
    Tests the slot paytable class.
    """
    def setUp(self):
        super(SlotPayTableTest, self).setUp()
        self.paytable = SlotPayTable()
        self.prizes = [
            {"pattern": ['A', 'A'], "multiplier": 0.15, "priority": 0},
            {"pattern": ['A', 'A', 'A'], "multiplier": 1.0, "priority": 1}
        ]

    def add_prizes_helper(self):
        """
        Helper method to add all declared prizes in
        :ref:self.prizes attribute.
        """
        for prize in self.prizes:
            self.paytable.add_prize(
                prize['pattern'],
                prize['multiplier'],
                prize['priority']
            )

    def test_add_prize(self):
        """
        Should store the given symbol pattern and the multiplier
        on its internal list.
        """
        self.add_prizes_helper()
        self.assertEqual(len(self.paytable.prizes), 2)

        for prize in self.paytable.prizes:
            self.assertIn("pattern", prize.keys())
            self.assertIn("multiplier", prize.keys())
            self.assertIn("priority", prize.keys())

    def test_add_existing_prize(self):
        """
        Should raise an ExistingCombinationException exception.
        """
        prize = self.prizes[0]
        with self.assertRaises(ExistingCombinationException):
            for i in range(2):
                self.paytable.add_prize(
                    prize['pattern'],
                    prize['multiplier'],
                    prize['priority']
                )

    def test_get_prizes_values(self):
        """
        Should return all possible prize values.
        """
        self.add_prizes_helper()
        values = list(self.paytable.get_prizes_values())
        assertion_values = [v["multiplier"] for v in self.prizes]
        self.assertEqual(len(values), len(self.prizes))
        for value in values:
            self.assertIn(value, assertion_values)

    def test_get_prize(self):
        """
        Should return the valid pattern for a given prize value.
        If no pattern exists for the given value, returns None.
        If there is two different patterns with same value, the
        higher priority will be returned.
        """
        # test a simple prize
        self.paytable.add_prize(['A'], 0.1, 0)
        prize = self.paytable.get_prize(0.1)
        self.assertEqual(prize['pattern'], ['A'])
        self.assertEqual(prize['priority'], 0)

        # test the call with a higher priority pattern
        # registered with same multiplier
        self.paytable.add_prize(['A', 'A'], 0.1, 1)
        prize = self.paytable.get_prize(0.1)
        self.assertEqual(prize['pattern'], ['A', 'A'])
        self.assertEqual(prize['priority'], 1)

        # test the call with invalid multiplier
        prize = self.paytable.get_prize(200)
        self.assertIsNone(prize)
