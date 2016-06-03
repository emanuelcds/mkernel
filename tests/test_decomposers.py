from unittest import TestCase

class SlotPrizeDecomposerTest(TestCase):

    def setUp(self):
        super(SlotPrizeDecomposerTest, self).setUp()

    def test_decompose_no_prize(self):
        """
        If value is ZERO, should return empty prize object.
        """
        pass

    def test_decompose_exact_prize(self):
        """
        If there is a match for exact prize, should
        return decomposed prizes into prize object.
        """
        pass

    def test_decompose_not_exact(self):
        """
        If there is a rest that can't be paid on paytable,
        should trigger bonus and return as bonus value.
        """
        pass
