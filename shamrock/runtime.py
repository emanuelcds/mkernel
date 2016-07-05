import os
import json

from shamrock.paytable import SlotPayTable
from shamrock.decomposers import SlotPrizeDecomposer


class SlotRuntime(object):
    """
    Class that runs slot machine games.
    """
    def __init__(self, config):
        # Sanity Check
        if not os.path.exists(config):
            raise Exception("Invalid file path: {}".format(config))
        with open(config, "r") as fp:
            self.settings = json.load(fp)
        fields = ['host', 'user', 'port', 'password', 'games']
        for field in fields:
            if not self.check_config(field):
                raise Exception("Field '{}' not declared in settings!".format(
                    field
                ))

        # Database Settings
        self.database = {
            "HOST": self.settings.get("host"),
            "USERNAME": self.settings.get("username"),
            "PASSWORD": self.settings.get("password"),
            "DATABASE": self.settings.get("database"),
            "PORT": self.settings.get("port"),
        }

        # Game Settings
        self.games = {}

        games = self.settings.get("games")

        for game in games:
            self.load_game(game)

    def check_config(self, key):
        if not self.settings:
            raise Exception("Settings not loaded!")
        return bool(self.settings.get(key, False))

    def load_game(self, game_settings):
        code = game_settings.get("code", False)
        name = game_settings.get("name", False)
        pool = game_settings.get("pool", False)
        lines = game_settings.get("lines", False)
        paytable = game_settings.get("paytable", False)
        if not code or not name or not pool or not lines or not paytable:
            raise Exception("Game Error: Required fields are {}".format(
                "code, name, pool, lines and paytable."
            ))

        ptable = SlotPayTable()
        ptable.from_dict(paytable)
        decomposer = SlotPrizeDecomposer(ptable)
        self.games[code] = {
            "name": name,
            "pool": pool,
            "lines": lines,
            "paytable": ptable,
            "decomposer": decomposer
        }

    def handle(self, code, bet):
        if code not in self.games.keys():
            return False
        return {}
