import os

from unittest import TestCase
from unittest.mock import MagicMock
from unittest.mock import patch

from shamrock.runtime import SlotRuntime


class SlotRuntimeTestCase(TestCase):

    def setUp(self):
        super().setUp()
        self.runtime = SlotRuntime(os.path.join(os.path.dirname(__file__), 'fixtures', 'settings.json'))
