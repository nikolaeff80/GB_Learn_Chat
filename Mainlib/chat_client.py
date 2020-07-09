import datetime
from socketserver import socket
# import sys

from Log.Log_decorators import log
from Log.client_log_config import client_log
from Mainlib import chat_config
from Mainlib.JIM import json_pack
from Mainlib.user import User


def echo_client():
    # Начиная с Python 3.2 сокеты имеют протокол менеджера контекста
    # При выходе из оператора with сокет будет авторматически закрыт
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:  # Создать сокет TCP
        sock.connect(('localhost', 7777))  # Соединиться с сервером
        while True:
            msg = input('Ваше сообщение: ')
            if msg == 'exit':
                break
            sock.send(msg.encode('utf-8'))  # Отправить!
            data = sock.recv(1024).decode('utf-8')
            print('Ответ:', data)


class ChatClient:

    def __init__(self, args, options_file):
        conf = self._get_options(args, options_file)
        self.host = conf['DEFAULT']['HOST']
        self.port = conf['DEFAULT']['PORT']

    # def send(self):
    #     try:
    #         sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #         sock.connect((self.host, self.port))
    #     except socket.error:
    #         sys.exit(2)
    #     msg = self._auth()
    #     client_log.info(f'Сообщение клиента {msg}')
    #     sock.sendall(msg)
    #
    #     try:
    #         msg = sock.recv(1024)
    #     except socket.timeout:
    #         print('Close connection by timeout.')
    #
    #     if not msg:
    #         client_log.warning('No response')
    #
    #     sock.close()

    @log
    def _get_options(self, args, options_file):
        """
        Get server config
        :param args: Command line arguments
        :param options_file: Config file name
        :return: dict
        """
        options = chat_config.get_json_options(options_file)
        cl_options = chat_config.get_cmd_options(args, 'a:p:')
        for opt in cl_options:
            if opt[0] == '-a':
                options['DEFAULT']['HOST'] = opt[1]
            elif opt[0] == '-p':
                options['DEFAULT']['PORT'] = opt[1]
        client_log.info(f'Аргументы для запуска {options}')
        return options

    def _get_user(self):
        return User('User', 'Password')

    @log
    def _auth(self):
        user = self._get_user()
        time = datetime.datetime.now()
        msg = {
            "action": "authenticate",
            "time": time.isoformat(),
            "user": {
                "account_name": user.name,
                "password": user.password,
            },
        }
        client_log.info(msg)
        return json_pack(msg)
