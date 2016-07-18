from unittest import TestCase
from shamrock.paytable import SlotPayTable


class SlotPayTableTest(TestCase):
    """
    Tests the slot paytable class.
    """
    def setUp(self):
        super(SlotPayTableTest, self).setUp()
        self.paytable = SlotPayTable()
        self.prizes = [
            {"pattern": ['A', 'A'], "multiplier": 0.15},
            {"pattern": ['A', 'A', 'A'], "multiplier": 1.0}
        ]
        self.paytable.from_dict(self.prizes)

    def test_from_dict(self):
        """
        Should load all prizes and sort by multiplier value.
        """
        self.paytable.from_dict(self.prizes)
        self.assertEqual(self.paytable.prizes[0].get("multiplier"), 1.00)
        self.assertEqual(self.paytable.prizes[1].get("multiplier"), 0.15)

    def test_get_prizes_values(self):
        """
        Should return all possible prize values.
        """
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
        prize = self.paytable.get_prize(0.15)
        self.assertEqual(prize['pattern'], ['A', 'A'])

        # test the call with a higher priority pattern
        # registered with same multiplier
        prize = self.paytable.get_prize(1.00)
        self.assertEqual(prize['pattern'], ['A', 'A', 'A'])

        # test the call with invalid multiplier
        prize = self.paytable.get_prize(200)
        self.assertIsNone(prize)
