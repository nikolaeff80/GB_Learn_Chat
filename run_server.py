import sys

from Log.server_log_config import server_log
from Mainlib.chat_server import ChatServer


config = 'config_server.json'
server = ChatServer(sys.argv, config)


if __name__ == "__main__":
    try:
        server_log.info('Server run...')
        server.mainloop()
    except KeyboardInterrupt as e:
        server_log.info('Server shutdown...')
        server.shutdown()
