import logging
import os
import sys

from Mainlib.chat_server import ChatServer

server_log = logging.getLogger('server-log')

PATH = os.path.dirname(os.path.abspath(__file__))
print(PATH)
PATH = os.path.join(PATH, 'Mainlib\config_server.json')
print(PATH)

print((os.getcwd()))
config = 'config_server.json'
server = ChatServer(sys.argv, config)

if __name__ == "__main__":
    try:
        server_log.info('Server run...')
        server.main()
    except KeyboardInterrupt as e:
        server_log.info('Server shutdown...')
        server.shutdown()
