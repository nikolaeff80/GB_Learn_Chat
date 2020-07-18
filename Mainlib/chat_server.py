"""Программа-сервер"""
import logging
import socketserver
import select

from socket import socket, AF_INET, SOCK_STREAM
from Log.Log_decorators import log
from Mainlib import JIM, chat_config
from Mainlib.JIM import JimResponse

# Инициализация логирования сервера.

server_log = logging.getLogger('server_log')


class MessengerHandler(socketserver.BaseRequestHandler):
    clients = set()

    @log
    def handle(self):
        data = self.request.recv(1024).strip()
        server_log.info(f'Получено от клиента: {data}')
        self.clients.add(self.request)
        if JIM.json_unpack(data):
            self.request.sendall(JimResponse.status_200(data))


def write_responses(responses, w_clients, all_clients):
    """Эхо-ответ сервера клиентам, от которых были запросы."""
    for sock in w_clients:
        if sock in responses:
            try:
                # Подготовить и отправить ответ сервера
                resp = responses[sock].encode('utf-8')
                # Эхо-ответ сделаем чуть непохожим на оригинал
                test_len = sock.send(resp.upper())
            except:  # Сокет недоступен, клиент отключился
                server_log.info('Клиент {} {} отключился'.format(sock.fileno(), sock.getpeername()))
                print('Клиент {} {} отключился'.format(sock.fileno(), sock.getpeername()))
                sock.close()
                all_clients.remove(sock)


def read_requests(r_clients, all_clients):
    """Чтение запросов из списка клиентов."""
    responses = {}  # Словарь ответов сервера вида {сокет: запрос}

    for sock in r_clients:
        try:
            data = sock.recv(1024).decode('utf-8')
            responses[sock] = data
        except:
            server_log.info('Клиент {} {} отключился'.format(sock.fileno(), sock.getpeername()))
            print('Клиент {} {} отключился'.format(sock.fileno(), sock.getpeername()))
            all_clients.remove(sock)
    if len(responses) != 0:
        server_log.info(f'Ответ сервера: {responses}')
    else:
        pass
    return responses


class ChatServer:

    def __init__(self, args, options_file):
        conf = self._get_options(args, options_file)
        self.host = conf['DEFAULT']['HOST']
        self.port = conf['DEFAULT']['PORT']
        self.server = None

    @log
    def main(self):
        """Основной цикл обработки запросов клиентов."""
        address = ('', 7777)
        clients = []
        messages = []
        names = dict()

        s = socket(AF_INET, SOCK_STREAM)
        s.bind(address)
        s.listen(20)
        s.settimeout(0.5)  # Таймаут для операций с сокетом
        while True:
            try:
                client, client_address = s.accept()  # Проверка подключений
            except OSError as e:
                pass  # timeout вышел
            else:
                server_log.info('Получен запрос на соединение от %s' % str(client_address))
                clients.append(client)
            finally:
                # Проверить наличие событий ввода-вывода
                wait = 0
                r = []
                w = []
                try:
                    r, w, e = select.select(clients, clients, [], wait)
                except:
                    pass  # Ничего не делать, если какой-то клиент отключился

                responses = read_requests(r, clients)  # Сохраним запросы клиентов
                if len(responses) != 0:
                    server_log.info(f'Запросы клиентов: {responses}')
                else:
                    pass
                write_responses(responses, w, clients)  # Выполним отправку ответов клиентам

    def run(self):
        """
        Run server
        :return:
        """
        server_log.info(f'Сервер запущен по адресу {self.host} порт {self.port}')
        self.server = socketserver.TCPServer((self.host, self.port), MessengerHandler)
        self.server.serve_forever()

    @log
    def shutdown(self):
        """
        Shutdown server
        :return:
        """
        server_log.info('Server shutdown')
        self.server.shutdown()

    @log
    def _get_options(self, args, options_file):
        """
        :param args:
        :param options_file:
        :return:
        """
        options = chat_config.get_json_options(options_file)
        cl_options = chat_config.get_cmd_options(args, "a:p:")
        for opt in cl_options:
            if opt[0] == "-a":
                options['DEFAULT']['HOST'] = opt[1]
            elif opt[0] == "-p":
                options['DEFAULT']['PORT'] = opt[1]
        server_log.debug(f'Аргументы командной строки, если не заданы, то default: {options}')
        return options

# from Mainlib.JIM import JimResponse, send_message, get_message
# from Mainlib.variables import ACTION, TIME, USER, ACCOUNT_NAME, PRESENCE, MESSAGE, MESSAGE_TEXT, SENDER, \
#     DESTINATION, EXIT

# @log
# def process_client_message(message, messages_list, client, clients, names):
#     """
#     Обработчик сообщений от клиентов, принимает словарь - сообщение от клиента,
#     проверяет корректность, отправляет словарь-ответ в случае необходимости.
#     :param message:
#     :param messages_list:
#     :param client:
#     :param clients:
#     :param names:
#     :return:
#     """
#     LOGGER.debug(f'Разбор сообщения от клиента : {message}')
#     # Если это сообщение о присутствии, принимаем и отвечаем
#     if ACTION in message and message[ACTION] == PRESENCE and \
#             TIME in message and USER in message:
#         # Если такой пользователь ещё не зарегистрирован,
#         # регистрируем, иначе отправляем ответ и завершаем соединение.
#         if message[USER][ACCOUNT_NAME] not in names.keys():
#             names[message[USER][ACCOUNT_NAME]] = client
#             send_message(client, JimResponse.status_200)
#         else:
#             response = JimResponse.status_401
#             send_message(client, response)
#             clients.remove(client)
#             client.close()
#         return
#     # Если это сообщение, то добавляем его в очередь сообщений.
#     # Ответ не требуется.
#     elif ACTION in message and message[ACTION] == MESSAGE and DESTINATION in message and TIME in message \
#             and SENDER in message and MESSAGE_TEXT in message:
#         messages_list.append(message)
#         return
#     # Если клиент выходит
#     elif ACTION in message and message[ACTION] == EXIT and ACCOUNT_NAME in message:
#         clients.remove(names[message[ACCOUNT_NAME]])
#         names[message[ACCOUNT_NAME]].close()
#         del names[message[ACCOUNT_NAME]]
#         return
#     # Иначе отдаём Bad request
#     else:
#         response = JimResponse.status_400
#         send_message(client, response)
#         return
#
#
# @log
# def process_message(message, names, listen_socks):
#     """
#     Функция адресной отправки сообщения определённому клиенту. Принимает словарь сообщение,
#     список зарегистрированых пользователей и слушающие сокеты. Ничего не возвращает.
#     :param message:
#     :param names:
#     :param listen_socks:
#     :return:
#     """
#     if message[DESTINATION] in names and names[message[DESTINATION]] in listen_socks:
#         send_message(names[message[DESTINATION]], message)
#         LOGGER.info(f'Отправлено сообщение пользователю {message[DESTINATION]} '
#                     f'от пользователя {message[SENDER]}.')
#     elif message[DESTINATION] in names and names[message[DESTINATION]] not in listen_socks:
#         raise ConnectionError
#     else:
#         LOGGER.error(
#             f'Пользователь {message[DESTINATION]} не зарегистрирован на сервере, '
#             f'отправка сообщения невозможна.')
#
#
# @log
# def arg_parser():
#     """Парсер аргументов коммандной строки"""
#     parser = argparse.ArgumentParser()
#     parser.add_argument('-p', default=7777, nargs='?')
#     parser.add_argument('-a', default='127.0.0.1', nargs='?')
#     namespace = parser.parse_args(sys.argv[1:])
#     listen_address = namespace.a
#     listen_port = namespace.p
#
#     # проверка получения корретного номера порта для работы сервера.
#     if not 1023 < listen_port < 65536:
#         LOGGER.critical(
#             f'Попытка запуска сервера с указанием неподходящего порта {listen_port}. '
#             f'Допустимы адреса с 1024 до 65535.')
#         sys.exit(1)
#
#     return listen_address, listen_port
#
#
# def main():
#     """
#     Загрузка параметров командной строки, если нет параметров, то задаём значения по умоланию
#     :return:
#     """
#     listen_address, listen_port = arg_parser()
#
#     LOGGER.info(
#         f'Запущен сервер, порт для подключений: {listen_port}, '
#         f'адрес с которого принимаются подключения: {listen_address}. '
#         f'Если адрес не указан, принимаются соединения с любых адресов.')
#     # Готовим сокет
#     transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     transport.bind((listen_address, listen_port))
#     transport.settimeout(0.5)
#
#     # список клиентов , очередь сообщений
#     clients = []
#     messages = []
#
#     # Словарь, содержащий имена пользователей и соответствующие им сокеты.
#     names = dict()
#
#     # Слушаем порт
#     transport.listen(10)
#     # Основной цикл программы сервера
#     while True:
#         # Ждём подключения, если таймаут вышел, ловим исключение.
#         try:
#             client, client_address = transport.accept()
#         except OSError:
#             pass
#         else:
#             LOGGER.info(f'Установлено соедение с ПК {client_address}')
#             clients.append(client)
#
#         recv_data_lst = []
#         send_data_lst = []
#         err_lst = []
#         # Проверяем на наличие ждущих клиентов
#         try:
#             if clients:
#                 recv_data_lst, send_data_lst, err_lst = select.select(clients, clients, [], 0)
#         except OSError:
#             pass
#
#         # принимаем сообщения и если ошибка, исключаем клиента.
#         if recv_data_lst:
#             for client_with_message in recv_data_lst:
#                 try:
#                     process_client_message(get_message(client_with_message),
#                                            messages, client_with_message, clients, names)
#                 except Exception:
#                     LOGGER.info(f'Клиент {client_with_message.getpeername()} '
#                                 f'отключился от сервера.')
#                     clients.remove(client_with_message)
#
#         # Если есть сообщения, обрабатываем каждое.
#         for i in messages:
#             try:
#                 process_message(i, names, send_data_lst)
#             except Exception:
#                 LOGGER.info(f'Связь с клиентом с именем {i[DESTINATION]} была потеряна')
#                 clients.remove(names[i[DESTINATION]])
#                 del names[i[DESTINATION]]
#         messages.clear()
#
#
# if __name__ == '__main__':
#     main()
