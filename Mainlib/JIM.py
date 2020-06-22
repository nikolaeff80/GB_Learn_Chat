import json


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


class JIM:
    pass


class JimMessage(JIM):
    pass


class JimResponse(JIM):

    def status_200(self):
        msg = {
            "response": 200,
            "alert": "Необязательное сообщение/уведомление"
        }
        return json_pack(msg)

    def status_402(self):
        msg = {
            "response": 402,
            "error": "This could be wrong password or no account with that name"
        }
        return json_pack(msg)
