from unittest import TestCase
from mock import MagicMock
from mock import call

from shamrock.decomposers import SlotPrizeDecomposer


class SlotPrizeDecomposerTest(TestCase):

    def setUp(self):
        super(SlotPrizeDecomposerTest, self).setUp()
        self.prizes = {
            0.25: ['A', 'A'],
            0.5:  ['A', 'A', 'A'],
            1:    ['A', 'A', 'A', 'A'],
        }

    def test_decompose_exact_prize(self):
        """
        If there is a match for exact prize, should
        return decomposed prizes into prize list.
        """
        # create a mock paytable
        ptable = MagicMock()
        ptable.get_prize.side_effect = lambda arg: self.prizes.get(arg, None)
        ptable.get_prizes_values.return_value = self.prizes.keys()
        # define bet and won
        bet, multiplier = (100, 1)
        # create decomposer
        decomposer = SlotPrizeDecomposer(ptable)
        # call decomposer with single prize
        prize = decomposer.decompose(bet, multiplier)
        # assert get_prizes_values method was called
        self.assertTrue(ptable.get_prizes_values.called)
        # assert get_prize was called once
        ptable.get_prize.assert_called_once_with(multiplier)
        # assert it decomposed with prizes array and exceeded values
        self.assertIn("prizes", prize)
        self.assertIn("exceeded", prize)
        self.assertEqual(len(prize.get("prizes")), 1)
        self.assertListEqual(prize.get("prizes")[0]["pattern"],
                             self.prizes.get(multiplier))
        self.assertEqual(prize.get("prizes")[0]["won"], multiplier * bet)
        self.assertEqual(prize.get("exceeded"), 0)

    def test_decompose_no_prize(self):
        """
        Should return empty prize array with all spent credits
        multiplied by multiplier on exceeded field.
        """
        # create a mock paytable
        ptable = MagicMock()
        ptable.get_prize.side_effect = lambda arg: self.prizes.get(arg, None)
        ptable.get_prizes_values.return_value = self.prizes.keys()
        # define bet and won
        bet, multiplier = (200, 0.1)
        # create decomposer
        decomposer = SlotPrizeDecomposer(ptable)
        # call decomposer with single prize
        prize = decomposer.decompose(bet, multiplier)
        # assert get_prizes_values method was called
        self.assertTrue(ptable.get_prizes_values.called)
        # assert get prize was not called
        ptable.get_prize.assert_not_called()
        # assert it decomposed with prizes array and exceeded values
        self.assertIn("prizes", prize)
        self.assertIn("exceeded", prize)
        self.assertEqual(len(prize.get("prizes")), 0)
        self.assertEqual(prize.get("exceeded"), multiplier)

    def test_decompose_multiple_prizes(self):
        """
        If there is a rest that can't be paid on paytable,
        should trigger bonus and return as bonus value.
        """
        # create a mock paytable
        ptable = MagicMock()
        ptable.get_prize.side_effect = lambda arg: self.prizes.get(arg, None)
        ptable.get_prizes_values.return_value = self.prizes.keys()
        # define bet and won
        bet, multiplier = (200, 0.1)
        # create decomposer
        decomposer = SlotPrizeDecomposer(ptable)
        # call decomposer with single prize
        prize = decomposer.decompose(bet, multiplier)
        # assert get_prizes_values method was called
        self.assertTrue(ptable.get_prizes_values.called)
        # assert get prize was not called
        ptable.get_prize.assert_not_called()
        # assert it decomposed with prizes array and exceeded values
        self.assertIn("prizes", prize)
        self.assertIn("exceeded", prize)
        self.assertEqual(len(prize.get("prizes")), 0)
        self.assertEqual(prize.get("exceeded"), multiplier)

    def test_decompose_exceeded_multiplier(self):
        """
        Should output exceeded value
        """
        # create a mock paytable
        ptable = MagicMock()
        ptable.get_prize.side_effect = lambda arg: self.prizes.get(arg, None)
        ptable.get_prizes_values.return_value = self.prizes.keys()
        # define bet, won and expected exceeded value
        bet, multiplier = (200, 2.5)
        expected = 0.75
        # create decompose
        decomposer = SlotPrizeDecomposer(ptable)
        prize = decomposer.decompose(bet, multiplier)
        self.assertTrue(ptable.get_prizes_values.called)
        prize_calls = [call(1), call(0.5), call(0.25)]
        ptable.get_prize.assert_has_calls(prize_calls)
        self.assertIn("prizes", prize)
        self.assertIn("exceeded", prize)
        self.assertEqual(len(prize.get("prizes")), 3)
        self.assertEqual(prize.get("exceeded"), expected)
