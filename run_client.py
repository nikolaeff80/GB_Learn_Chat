import sys

from GB_Learning_chat.Mainlib.chat_client import ChatClient

config = "config_client.json"

if __name__ == "__main__":
    client = ChatClient(sys.argv, config)
    client.send()
