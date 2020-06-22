import datetime
import socket
import sys

from GB_Learning_chat.Mainlib import chat_config
from GB_Learning_chat.Mainlib.JIM import json_pack, json_unpack
from GB_Learning_chat.Mainlib.user import User


class ChatClient:

    def __init__(self, args, options_file):
        conf = self.__get_options(args, options_file)
        self.host = conf['DEFAULT']['HOST']
        self.port = conf['DEFAULT']['PORT']

    def send(self):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((self.host, self.port))
        except socket.error as err:
            print("Connection error: {}".format(err))
            sys.exit(2)
        print("create socket...")
        msg = self.__auth()
        sock.sendall(msg)
        print("send message...")

        try:
            msg = sock.recv(1024)
            print(json_unpack(msg))
        except socket.timeout:
            print("Close connection by timeout.")

        if not msg:
            print("No response")

        sock.close()
        print("client close...")

    def __get_options(self, args, options_file):
        """
        Get server config
        :param args: Command line arguments
        :param options_file: Config file name
        :return: dict
        """
        options = chat_config.get_json_options(options_file)
        cl_options = chat_config.get_cmd_options(args, "a:p:")
        for opt in cl_options:
            if opt[0] == "-a":
                options['DEFAULT']['HOST'] = opt[1]
            elif opt[0] == "-p":
                options['DEFAULT']['PORT'] = opt[1]
        return options

    def __get_user(self):
        return User("User", "Password")

    def __auth(self):
        user = self.__get_user()
        time = datetime.datetime.now()
        msg = {
            "action": "authenticate",
            "time": time.isoformat(),
            "user": {
                "account_name": user.name,
                "password": user.password,
            },
        }
        return json_pack(msg)
