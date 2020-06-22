import sys

from GB_Learning_chat.Mainlib.chat_server import ChatServer

config = "config_server.json"

if __name__ == "__main__":
    server = ChatServer(sys.argv, config)
    try:
        print("Server run...")
        server.run()
    except KeyboardInterrupt as e:
        print("Server shutdown...")
        server.shutdown()
