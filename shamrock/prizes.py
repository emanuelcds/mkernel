import random
from shamrock.exceptions import MaxWildException


class SlotPrize(object):

    def __init__(self, paylines, symbols, decomposition, freespin=False):
        """
            Builds prize output based on
            prize list and line patterns.
            @param paylines list of payline patterns from game configuration
            @param symbols list of game symbols
            @param decomposition dictionary with prizes, freespins and bonus
            @param freespin flag informing if current prize is reelstop from a
            freespin bonus round
            @return Prize object serialized containing:
                - total_win: amount of credits won on the given prize
                - reelstops: matrix containing the symbols on the reels,
                - paylines: list of lines with prize and amount
                    won on each one,
                - antecipation: which reels should animate antecipation prize
                - freespins: freespin plays (empty if no freespin at all)
                - bonus: bonus steps (empty if no bonus at all)
        """
        # initialize values
        self.total_win = 0
        self.reelstops = [
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0],
        ]
        self.lines = []
        self.paylines = list(paylines)
        self.antecipation = []
        self.bonus = decomposition.get("bonus", [])
        self.raw_freespins = decomposition.get("freespins", [])
        self.freespins = []
        self.symbols = symbols
        prizes = list(decomposition.get("prizes", []))

        # if amount of wilds equals minimum matches, should retry as freespin
        self.wild_amount = 0
        self.min_matches = 0
        if len(prizes) > 0:
            self.min_matches = min([len(p["pattern"]) for p in prizes])

        if len(prizes) > len(paylines):
            raise Exception("Cannot map {} prizes to {} lines!".format(
                len(prizes), len(paylines)
            ))

        while len(prizes) > 0:
            # process each prize
            self.__process_prizes(prizes.pop())
            if self.wild_amount >= self.min_matches and not freespin:
                raise MaxWildException(
                    "Cannot override a whole prize with wilds! ({})".format(
                        self.wild_amount
                    )
                )

    def __process_prizes(self, prize):
        """
        Process prizes and render them on reelstops matrix.
        """
        is_bonus = prize.get("bonus", False)
        is_freespin = prize.get("scatter", False)
        is_basegame = not is_freespin and not is_bonus
        # get unused payline
        payline = random.choice(self.paylines)
        if is_basegame:
            self.paylines.remove(payline)
        # iterates over pattern and fill reelstops with the given payline
        for idx, symbol in enumerate(prize["pattern"]):
            reel_pos = payline["pattern"][idx]
            # if reel position already filled, assign wild,
            # otherwise, fill in the prize symbol
            if self.reelstops[idx][reel_pos]:
                self.reelstops[idx][reel_pos] = "W"
                self.wild_amount += 1
            else:
                self.reelstops[idx][reel_pos] = symbol
        # generates line
        line = {
            # normalizing pattern indexes for -1 0 1 notation
            "indexes": [x - 1 for x in payline["pattern"]],
            "line": payline["line"],
            "matches": len(prize["pattern"]),
            "win": 0
        }
        # updates total win and amount won on the current line
        if is_freespin:
            self.__process_freespins(self.raw_freespins)
            # amount of freespins are multiplied by scatters
            # so, antecipation runs for the last three reels
            # (reels are zero indexed)
            self.antecipation = [2, 3, 4]
        elif is_bonus:
            self.total_win += sum(self.bonus)
            line["win"] = sum(self.bonus)
            line["bonus"] = True
            # always three or more bonus are sufficient
            # so, anticipation makes mystery for the third reel
            # (reels are zero indexed)
            self.antecipation = [2]
        else:
            line["win"] = prize["won"]
            self.total_win += prize["won"]
        # add line to paylines
        self.lines.append(line)

    def __process_freespins(self, spins):
        self.freespins = []
        while len(spins) > 0:
            reelstops = [
                [0, 0, 0],
                [0, 0, 0],
                [0, 0, 0],
                [0, 0, 0],
                [0, 0, 0],
            ]
            prize = spins.pop()
            lines = []
            paylines = self.paylines[:]
            total_win = 0
            if prize["won"]:
                payline = random.choice(paylines)
                paylines.remove(payline)
                # iterates over pattern and fill reelstops with the
                # given payline
                for idx, symbol in enumerate(prize["pattern"]):
                    reel_pos = payline["pattern"][idx]
                    # if reel position already filled, assign wild,
                    # otherwise, fill in the prize symbol
                    if reelstops[idx][reel_pos]:
                        reelstops[idx][reel_pos] = "W"
                    else:
                        reelstops[idx][reel_pos] = symbol
                # generates line
                line = {
                    # normalizing pattern indexes for -1 0 1 notation
                    "indexes": [x - 1 for x in payline["pattern"]],
                    "line": payline["line"],
                    "matches": len(prize["pattern"]),
                    "win": prize["won"]
                }
                lines.append(line)
                total_win += prize["won"]
                self.total_win += total_win
            self.fill(reelstops, list(self.symbols))
            self.freespins.append({
                "total_win": float("%.2f" % (total_win)),
                "reelstops": reelstops,
                "paylines": lines,
            })

    def fill(self, reelport, symbols):
        for i, reel in enumerate(reelport):
            previous_reel = []
            # get last reel symbols if exists
            if i > 0:
                previous_reel = [s for s in reelport[i-1] if s]
            possible = [s for s in symbols if s not in previous_reel]
            for k, symbol in enumerate(reel):
                if not symbol:
                    reelport[i][k] = random.choice(possible)

    def serialize(self):
        """
        Serializes the given prize into a dictionary.
        """
        # fill in holes in reel with random symbols
        self.fill(self.reelstops, self.symbols)
        # return serialized prize
        return {
            "total_win": float("%.2f" % self.total_win),
            "reelstops": self.reelstops,
            "paylines": self.lines,
            "freespins": self.freespins,
            "bonus": self.bonus,
            "antecipation": self.antecipation if self.antecipation else []
        }
