"""Программа-клиент"""


import datetime
import logging
import sys
from socketserver import socket
# import sys

from Log.Log_decorators import log
from Mainlib import chat_config
from Mainlib.JIM import json_pack
from Mainlib.user import User

# Инициализация логирования клиента
client_log = logging.getLogger('client_log')


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

    def send(self):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((self.host, self.port))
        except socket.error:
            sys.exit(2)
        msg = self._auth()
        client_log.info(f'Сообщение клиента {msg}')
        sock.sendall(msg)

        try:
            msg = sock.recv(1024)
        except socket.timeout:
            print('Close connection by timeout.')

        if not msg:
            client_log.warning('No response')

        sock.close()

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


# import logging
# import sys
# import json
# import socket
# import time
# import argparse
# import threading
#
#
# from Mainlib.JIM import send_message, get_message
# from Mainlib.variables import ACTION, SENDER, MESSAGE_TEXT, DESTINATION, MESSAGE, TIME, EXIT, ACCOUNT_NAME, PRESENCE, \
#     USER, RESPONSE, ERROR
#
# # Инициализация клиентского логера
# from Log.Log_decorators import log
#
#
# LOGGER = logging.getLogger('client_log')
#
#
# @log
# def create_exit_message(account_name):
#     """Функция создаёт словарь с сообщением о выходе"""
#     return {
#         ACTION: EXIT,
#         TIME: time.time(),
#         ACCOUNT_NAME: account_name
#     }
#
#
# @log
# def message_from_server(sock, my_username):
#     """Функция - обработчик сообщений других пользователей, поступающих с сервера"""
#     while True:
#         try:
#             message = get_message(sock)
#             if ACTION in message and message[ACTION] == MESSAGE and \
#                     SENDER in message and DESTINATION in message \
#                     and MESSAGE_TEXT in message and message[DESTINATION] == my_username:
#                 print(f'\nПолучено сообщение от пользователя {message[SENDER]}:'
#                       f'\n{message[MESSAGE_TEXT]}')
#                 LOGGER.info(f'Получено сообщение от пользователя {message[SENDER]}:'
#                             f'\n{message[MESSAGE_TEXT]}')
#             else:
#                 LOGGER.error(f'Получено некорректное сообщение с сервера: {message}')
#         except Exception:
#             LOGGER.error(f'Не удалось декодировать полученное сообщение.')
#         except (OSError, ConnectionError, ConnectionAbortedError,
#                 ConnectionResetError, json.JSONDecodeError):
#             LOGGER.critical(f'Потеряно соединение с сервером.')
#             break
#
#
# @log
# def create_message(sock, account_name):
#     """
#     Функция запрашивает кому отправить сообщение и само сообщение,
#     и отправляет полученные данные на сервер
#     :param sock:
#     :param account_name:
#     :return:
#     """
#     to_user = input('Введите получателя сообщения: ')
#     message = input('Введите сообщение для отправки: ')
#     message_dict = {
#         ACTION: MESSAGE,
#         SENDER: account_name,
#         DESTINATION: to_user,
#         TIME: time.time(),
#         MESSAGE_TEXT: MESSAGE
#     }
#     LOGGER.debug(f'Сформирован словарь сообщения: {message_dict}')
#     try:
#         send_message(sock, message_dict)
#         LOGGER.info(f'Отправлено сообщение для пользователя {to_user}')
#     except:
#         LOGGER.critical('Потеряно соединение с сервером.')
#         sys.exit(1)
#
#
# @log
# def user_interactive(sock, username):
#     """Функция взаимодействия с пользователем, запрашивает команды, отправляет сообщения"""
#     print_help()
#     while True:
#         command = input('Введите команду: ')
#         if command == 'message':
#             create_message(sock, username)
#         elif command == 'help':
#             print_help()
#         elif command == 'exit':
#             send_message(sock, create_exit_message(username))
#             print('Завершение соединения.')
#             LOGGER.info('Завершение работы по команде пользователя.')
#             # Задержка неоходима, чтобы успело уйти сообщение о выходе
#             time.sleep(0.5)
#             break
#         else:
#             print('Команда не распознана, попробойте снова. help - вывести поддерживаемые команды.')
#
#
# @log
# def create_presence(account_name):
#     """Функция генерирует запрос о присутствии клиента"""
#     out = {
#         ACTION: PRESENCE,
#         TIME: time.time(),
#         USER: {
#             ACCOUNT_NAME: account_name
#         }
#     }
#     LOGGER.debug(f'Сформировано {PRESENCE} сообщение для пользователя {account_name}')
#     return out
#
#
# def print_help():
#     """Функция выводящяя справку по использованию"""
#     print('Поддерживаемые команды:')
#     print('message - отправить сообщение. Кому и текст будет запрошены отдельно.')
#     print('help - вывести подсказки по командам')
#     print('exit - выход из программы')
#
#
# @log
# def process_response_ans(message):
#     """
#     Функция разбирает ответ сервера на сообщение о присутствии,
#     возращает 200 если все ОК или генерирует исключение при ошибке
#     :param message:
#     :return:
#     """
#     LOGGER.debug(f'Разбор приветственного сообщения от сервера: {message}')
#     if RESPONSE in message:
#         if message[RESPONSE] == 200:
#             return '200 : OK'
#         elif message[RESPONSE] == 400:
#             raise Exception(f'400 : {message[ERROR]}')
#     raise Exception(RESPONSE)
#
#
# @log
# def arg_parser():
#     """Парсер аргументов коммандной строки"""
#     parser = argparse.ArgumentParser()
#     parser.add_argument('addr', default='127.0.0.1', nargs='?')
#     parser.add_argument('port', default=7777, type=int, nargs='?')
#     parser.add_argument('-n', '--name', default=None, nargs='?')
#     namespace = parser.parse_args(sys.argv[1:])
#     server_address = namespace.addr
#     server_port = namespace.port
#     client_name = namespace.name
#
#     # проверим подходящий номер порта
#     if not 1023 < server_port < 65536:
#         LOGGER.critical(
#             f'Попытка запуска клиента с неподходящим номером порта: {server_port}. '
#             f'Допустимы адреса с 1024 до 65535. Клиент завершается.')
#         sys.exit(1)
#
#     return server_address, server_port, client_name
#
#
# class ServerError(Exception):
#     """Исключение - ошибка сервера"""
#     def __init__(self, text):
#         self.text = text
#
#     def __str__(self):
#         return self.text
#
#
# class ReqFieldMissingError(Exception):
#     """Ошибка - отсутствует обязательное поле в принятом словаре"""
#     def __init__(self, missing_field):
#         self.missing_field = missing_field
#
#     def __str__(self):
#         return f'В принятом словаре отсутствует обязательное поле {self.missing_field}.'
#
#
# def main():
#     """Сообщаем о запуске"""
#     print('Консольный месседжер. Клиентский модуль.')
#
#     # Загружаем параметы коммандной строки
#     server_address, server_port, client_name = arg_parser()
#
#     # Если имя пользователя не было задано, необходимо запросить пользователя.
#     if not client_name:
#         client_name = input('Введите имя пользователя: ')
#
#     LOGGER.info(
#         f'Запущен клиент с парамертами: адрес сервера: {server_address}, '
#         f'порт: {server_port}, имя пользователя: {client_name}')
#
#     # Инициализация сокета и сообщение серверу о нашем появлении
#     try:
#         transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#         transport.connect((server_address, server_port))
#         send_message(transport, create_presence(client_name))
#         answer = process_response_ans(get_message(transport))
#         LOGGER.info(f'Установлено соединение с сервером. Ответ сервера: {answer}')
#         print(f'Установлено соединение с сервером.')
#     except json.JSONDecodeError:
#         LOGGER.error('Не удалось декодировать полученную Json строку.')
#         sys.exit(1)
#     except ServerError as error:
#         LOGGER.error(f'При установке соединения сервер вернул ошибку: {error.text}')
#         sys.exit(1)
#     except ReqFieldMissingError as missing_error:
#         LOGGER.error(f'В ответе сервера отсутствует необходимое поле {missing_error.missing_field}')
#         sys.exit(1)
#     except (ConnectionRefusedError, ConnectionError):
#         LOGGER.critical(
#             f'Не удалось подключиться к серверу {server_address}:{server_port}, '
#             f'конечный компьютер отверг запрос на подключение.')
#         sys.exit(1)
#     else:
#         # Если соединение с сервером установлено корректно,
#         # запускаем клиентский процесс приёма сообщний
#         receiver = threading.Thread(target=message_from_server, args=(transport, client_name))
#         receiver.daemon = True
#         receiver.start()
#
#         # затем запускаем отправку сообщений и взаимодействие с пользователем.
#         user_interface = threading.Thread(target=user_interactive, args=(transport, client_name))
#         user_interface.daemon = True
#         user_interface.start()
#         LOGGER.debug('Запущены процессы')
#
#         # Watchdog основной цикл, если один из потоков завершён,
#         # то значит или потеряно соединение или пользователь
#         # ввёл exit. Поскольку все события обработываются в потоках,
#         # достаточно просто завершить цикл.
#         while True:
#             time.sleep(1)
#             if receiver.is_alive() and user_interface.is_alive():
#                 continue
#             break
#
#
# if __name__ == '__main__':
#     main()
