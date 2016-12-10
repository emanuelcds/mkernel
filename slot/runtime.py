import os
import json

from slot.paytable import SlotPayTable
from slot.decomposers import SlotPrizeDecomposer
from slot.prizes import SlotPrize
from slot.exceptions import MaxWildException


class SlotRuntime(object):
    """
    Class that runs slot machine games.
    """
    def __init__(self, config, BackendCls):
        # Sanity Check
        if not os.path.exists(config):
            raise Exception("Invalid file path: {}".format(config))
        with open(config, "r") as fp:
            self.settings = json.load(fp)
        fields = ['games']
        for field in fields:
            if not self.check_config(field):
                raise Exception("Field '{}' not declared in settings!".format(
                    field
                ))

        # Initializing Backend Adapter
        self.backend = BackendCls({})

        # Game Settings
        self.games = {}

        games = self.settings.get("games")

        for game in games:
            self.load_game(game)

        self.last_result = {}

    def check_config(self, key):
        if not self.settings:
            raise Exception("Settings not loaded!")
        return bool(self.settings.get(key, False))

    def load_game(self, game_settings):
        code = game_settings.get("code", False)
        name = game_settings.get("name", False)
        lines = game_settings.get("lines", False)
        symbols = game_settings.get("symbols", False)
        paytable = game_settings.get("paytable", False)
        if not (code and name and lines and symbols and paytable):
            raise Exception("Game Error: Required fields are {}".format(
                "code, name, lines and paytable."
            ))

        ptable = SlotPayTable()
        ptable.from_dict(paytable)
        decomposer = SlotPrizeDecomposer(ptable)
        self.games[code] = {
            "name": name,
            "lines": lines,
            "paytable": ptable,
            "decomposer": decomposer,
            "symbols": symbols,
        }

    def handle(self, code, bet):
        if code not in self.games.keys():
            return False
        game = self.games[code]
        decomposer = game["decomposer"]
        paylines = game["lines"]
        symbols = game["symbols"]
        credits = self.backend.get_credits()
        multiplier = self.backend.play(bet, game.get("code"))
        credits_after = self.backend.get_credits()

        # try to decompose the prize
        decomposed = decomposer.handle(bet, multiplier, paylines)
        try:
            result = SlotPrize(paylines, symbols, decomposed)
        except MaxWildException:
            decomposed = decomposer.handle(bet, multiplier, paylines, True)
            result = SlotPrize(paylines, symbols, decomposed)
        out = result.serialize()
        out["credits_before"] = credits
        out["credits_after"] = credits_after
        self.last_result = out
        return out

    def pre_review(self, code, bet):
        out = {}
        if code not in self.games.keys():
            out["error"] = "Invalid game."
        else:
            game = self.games[code]
            out["prize"] = self.backend.pre_reveal(bet, game.get("code"))
        return out
