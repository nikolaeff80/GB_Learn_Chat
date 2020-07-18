import json
import sys
from _multiprocessing import recv

from Log.Log_decorators import log


def json_pack(dict_msg):
    """
    Packing messages for sending over TCP
    :param dict_msg: dict
    :return: str
    """
    str_msg = json.dumps(dict_msg)
    return str_msg.encode("utf8")


def json_unpack(bt_str):
    """
    Unpacking a received message
    :param bt_str: str
    :return: dict
    """
    str_decoded = bt_str.decode('utf-8')
    return json.loads(str_decoded)


class JIM(object):
    pass



@log
def get_message(client):
    """
    Утилита приёма и декодирования сообщения принимает байты выдаёт словарь,
    если приняточто-то другое отдаёт ошибку значения
    :param client:
    :return:
    """
    encoded_response = client.recv(2048)
    if isinstance(encoded_response, bytes):
        json_response = encoded_response.decode('utf-8')
        response = json.loads(json_response)
        if isinstance(response, dict):
            return response
        else:
            raise Exception
    else:
        raise Exception


@log
def send_message(sock, message):
    """
    Утилита кодирования и отправки сообщения
    принимает словарь и отправляет его
    :param sock:
    :param message:
    :return:
    """
    if not isinstance(message, dict):
        raise Exception
    js_message = json.dumps(message)
    encoded_message = js_message.encode('utf-8')
    sock.send(encoded_message)


class JimResponse(JIM):

    def status_200(self):
        msg = {
            "response": 200,
            "alert": "Необязательное сообщение/уведомление"
        }
        return json_pack(msg)

    def status_400(self):
        msg = {
            "response": 400,
            "error": "Bad Request"
        }
        return json_pack(msg)

    def status_401(self):
        msg = {
            "response": 401,
            "error": "Name is already taken"
        }
        return json_pack(msg)

    def status_402(self):
        msg = {
            "response": 402,
            "error": "This could be wrong password or no account with that name"
        }
        return json_pack(msg)
