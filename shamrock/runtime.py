import os
import json
import random

from unittest import mock

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
            "host": self.settings.get("host"),
            "user": self.settings.get("username"),
            "password": self.settings.get("password"),
            "db": self.settings.get("database"),
            "port": self.settings.get("port"),
        }

        # Initializing Backend Adapter
        backend = SweepstakesBackend(**self.database)
        self.backend = backend

        # Game Settings
        self.games = {}

        games = self.settings.get("games")

        for game in games:
            self.load_game(game)

    def check_config(self, key):
        if not self.settings:
            raise Exception("Settings not loaded!")
        return bool(self.settings.get(key, False))

    def cash_in(self, amount):
        self.backend.set_credits(self.backend.credits + amount)

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
        game = self.games[code]
        decomposer = game["decomposer"]
        multiplier = self.backend.play(bet, game.get("pool"))
        return decomposer.decompose(bet, multiplier)


class SweepstakesBackend(object):
    """
    Connection to database pool.
    """

    def __init__(self, host=None, user=None, password=None,
                 db=None, port=None):
        self.credits = 0
        self.backend = mock.MagicMock()
        self.prizes = [
            1000, 1250, 15, 35, 75, 0, 0, 0,
            25, 85, 725, 0, 0, 0, 25, 20, 10,
            5, 15, 20, 25, 30, 35, 40, 45, 50,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        ]
        self.backend.play.side_effect = lambda: random.choice(self.prizes)

    def set_credits(self, credits):
        self.credits = credits

    def play(self, bet, pool):
        self.credits -= bet
        value = self.backend.play()
        self.credits += value * bet
        return value
