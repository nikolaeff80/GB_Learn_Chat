Mainlib module
======================

Пакет общих утилит, использующихся в разных модулях проекта.

Скрипт descriptors.py
---------------------

.. autoclass:: Mainlib.descriptors.Port
    :members:

.. autoclass:: Mainlib.descriptors.IPAddress
    :members:

Mainlib.descriptors **Port**

    For port number descriptor: Validating the port.

Mainlib.descriptors **IPAddress**

    The descriptor for the IP address: Validating the IP address

Скрипт exception.py
---------------------

.. autoclass:: Mainlib.exception.IncorrectDataRecivedError
   :members:

.. autoclass:: Mainlib.exception.ServerError
   :members:

.. autoclass:: Mainlib.exception.NonDictInputError
   :members:

.. autoclass:: Mainlib.exception.ReqFieldMissingError
   :members:

.. autoclass:: Mainlib.exception.DataBaseInteractiveError
   :members:

Скрипт verifier.py
-----------------------

.. autoclass:: Mainlib.verifier.ServerVerifier
   :members:

.. autoclass:: Mainlib.verifier.ClientVerifier
   :members:

Скрипт JIM.py
---------------------

Mainlib.JIM **get_message** (client)


    The utility for receiving and decoding a message accepts bytes and gives out a dictionary,
    if something else is received it gives a value error


Mainlib.JIM **send_message** (sock, message)


    Message encoding and sending utility,
    takes a dictionary and sends it


Скрипт variables.py
---------------------

Содержит разные глобальные переменные проекта.