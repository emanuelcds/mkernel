from shamrock.exceptions import ExistingCombinationException


class SlotPayTable(object):
    """
    Implements slot machine paytable logic suport.
    """

    def __init__(self):
        self.prizes = []

    def add_prize(self, pattern, multiplier, priority=0):
        """
        Adds new prize to the paytable.
        This prize will pay the amount specified in 'multiplier'.
        It will override any prize in the same line with lower
        priority.
        e.g:
            >>> add_prize(['A', 'A'], 0.25, 0)
            >>> add_prize(['A', 'A', 'A'], 0.5, 1) # has higher priority
        """
        # checks if prize already exists
        for prize in self.prizes:
            if prize["pattern"] == pattern:
                raise ExistingCombinationException("Pattern already exists!")
        self.prizes.append({
            "pattern": pattern,
            "multiplier": multiplier,
            "priority": priority
        })
        self.prizes.sort(key=lambda x: x["priority"], reverse=True)

    def get_prizes_values(self):
        """
        Returns a list of possible prizes from the given paytable.
        """
        for prize in self.prizes:
            yield prize["multiplier"]

    def get_prize(self, value):
        """
        Gets the available prize for the given value.
        If more than one prize is available, the prize
        with highest priority is returned.
        """
        for prize in self.prizes:
            if prize["multiplier"] == value:
                return prize
