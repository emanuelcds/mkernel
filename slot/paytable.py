from decimal import Decimal


class SlotPayTable(object):
    """
    Implements slot machine paytable logic suport.
    """

    def __init__(self):
        self.prizes = []

    def get_prizes_values(self):
        """
        Returns a list of possible prizes from the given paytable.
        """
        for prize in self.prizes:
            if prize.get("multiplier", False):
                yield Decimal(
                    "{0:.2f}".format(prize["multiplier"])
                )

    def get_prize(self, value):
        """
        Gets the available prize for the given value.
        If more than one prize is available, the prize
        with highest priority is returned.
        """
        for prize in self.prizes:
            prize_value = prize.get("multiplier", None)
            if prize_value:
                current_prize = Decimal("{0:.2f}".format(prize_value))
                if current_prize == value:
                    return prize
        return None

    def get_bonus(self):
        """
        Gets valid prize pattern for bonus.
        """
        for prize in self.prizes:
            if prize.get("bonus", False):
                return prize
        return None

    def get_freespins(self, amount):
        """
        Gets a valid freespin pattern for the given spins amount.
        """
        for prize in self.prizes:
            if prize.get("freespins", 0) >= amount:
                return prize
        return None

    def from_dict(self, prizes):
        """
        Loads paytable from dictionary.
        """
        self.prizes = prizes
        self.prizes.sort(key=lambda x: x.get("multiplier", 0), reverse=True)
