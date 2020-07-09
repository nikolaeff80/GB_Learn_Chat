import socketserver
import select

from socket import socket, AF_INET, SOCK_STREAM
from Log.Log_decorators import log
from Log.server_log_config import server_log
from Mainlib import JIM, chat_config
from Mainlib.JIM import JimResponse


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
    def mainloop(self):
        """Основной цикл обработки запросов клиентов."""
        address = ('', 7777)
        clients = []

        s = socket(AF_INET, SOCK_STREAM)
        s.bind(address)
        s.listen(20)
        s.settimeout(0.5)  # Таймаут для операций с сокетом
        while True:
            try:
                conn, addr = s.accept()  # Проверка подключений
            except OSError as e:
                pass  # timeout вышел
            else:
                print('Получен запрос на соединение от %s' % str(addr))
                clients.append(conn)
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
    # def run(self):
    #     """
    #     Run server
    #     :return:
    #     """
    #     server_log.debug(f'Сервер запущен по адресу {self.host} порт {self.port}')
    #     self.server = socketserver.TCPServer((self.host, self.port), MessengerHandler)
    #     self.server.serve_forever()

    @log
    def shutdown(self):
        """
        Shutdown server
        :return:
        """
        server_log.debug('Server shutdown')
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
