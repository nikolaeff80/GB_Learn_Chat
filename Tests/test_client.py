import unittest
from unittest import TestCase

from Mainlib.JIM import json_pack
from Mainlib.user import User


class TestChatClient(TestCase):

    def setUp(self):
        self.user = User('User', 'Password')
        self.args = {'HOST': '127.0.0.1', 'PORT': 7777}
        self.msg = {
            'action': 'authenticate',
            'user': {
                'account_name': self.user.name,
                'password': self.user.password,
            }}

    # def test_get_user(self):
    #     self.assertEqual(self.user, (User('User', 'Password')), msg='Ok')
    #     не понял почему объекты разные. Буду разбираться

    def test_auth(self):
        self.assertIsInstance(json_pack(self.msg), bytes, msg='Ok')

    def test_auth_count_equal(self):
        self.assertCountEqual(json_pack(self.msg),
                              b'{"action": "authenticate", "user": {"account_name": "User", "password": "Password"}}',
                              msg='Ok')

    if __name__ == "__main__":
        unittest.main()
