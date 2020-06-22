import socketserver

from GB_Learning_chat.Mainlib import JIM, chat_config
from GB_Learning_chat.Mainlib.JIM import JimResponse


class MessengerHandler(socketserver.BaseRequestHandler):
    clients = set()

    def handle(self):
        data = self.request.recv(1024).strip()
        print("{} wrote:".format(self.client_address[0]))
        print(data)
        self.clients.add(self.request)
        if JIM.json_unpack(data):
            self.request.sendall(JimResponse.status_200(data))


class ChatServer:

    def __init__(self, args, options_file):
        conf = self.__get_options(args, options_file)
        self.host = conf['DEFAULT']['HOST']
        self.port = conf['DEFAULT']['PORT']
        self.server = None

    def run(self):
        """
        Run server
        :return:
        """
        self.server = socketserver.TCPServer((self.host, self.port), MessengerHandler)
        self.server.serve_forever()

    def shutdown(self):
        """
        Shutdown server
        :return:
        """
        self.server.shutdown()

    def __get_options(self, args, options_file):
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
        return options
