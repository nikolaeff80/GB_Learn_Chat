import sys
import os
import logging

from Mainlib.chat_server import ChatServer

server_log = logging.getLogger('server_log')

server_log.info(os.getcwd())
config = 'config_server.json'
server = ChatServer(sys.argv, config)

if __name__ == "__main__":
    try:
        server_log.debug('Server run...')
        server.run()
    except KeyboardInterrupt as e:
        server_log.debug('Server shutdown...')
        server.shutdown()
