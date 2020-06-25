import unittest
import json
import sys

from Mainlib.chat_config import get_json_options
from Mainlib.chat_server import ChatServer


class TestChatConfig(unittest.TestCase):
    config = "config_server.json"
    server = ChatServer(sys.argv, config)
    test_dict = {'DEFAULT': {'HOST': '127.0.0.1', 'PORT': 7777}}

    def test_get_json_options_is(self):
        self.assertIsInstance(get_json_options(self.config), dict, msg='Ok')

    def test_get_json_options_equal(self):
        self.assertEqual(get_json_options(self.config), self.test_dict, msg='Ok')

