import unittest
from Mainlib.JIM import json_pack, json_unpack


class TestJIM(unittest.TestCase):

    msg = {
        "HOST": "127.0.0.1",
        "PORT": 7777
    }
    b_msg = b'{"action": "authenticate", "user": {"account_name": "User", "password": "Password"}}'

    def test_json_pack(self):
        self.assertIsInstance(json_pack(self.msg), bytes, msg='Ok')

    def test_json_unpack(self):
        self.assertIsInstance((json_unpack(self.b_msg)), dict, msg='Ok')
