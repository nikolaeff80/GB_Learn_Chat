import sys

from Mainlib.chat_client import ChatClient

config = "config_client.json"

if __name__ == "__main__":
    client = ChatClient(sys.argv, config)
    client.send()
