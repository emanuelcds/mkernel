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
                yield prize["multiplier"]

    def get_prize(self, value):
        """
        Gets the available prize for the given value.
        If more than one prize is available, the prize
        with highest priority is returned.
        """
        for prize in self.prizes:
            if prize.get("multiplier", "") == value:
                return prize
        return None

    def get_bonus(self, value):
        """
        Gets valid prize pattern for bonus.
        """
        for prize in self.prizes:
            if prize.get("bonus", False):
                return self.prize
        return None

    def get_freespins(self, amount):
        """
        Gets a valid freespin pattern for the given spins amount.
        """
        for prize in self.prizes:
            if prize.get("freespins", 0) >= amount:
                return self.prize
        return None

    def from_dict(self, prizes):
        """
        Loads paytable from dictionary.
        """
        self.prizes = prizes
        self.prizes.sort(key=lambda x: x.get("multiplier", 0), reverse=True)
