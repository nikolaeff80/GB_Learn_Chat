Client module documentation
=================================================

Клиентское приложение для обмена сообщениями. Поддерживает
отправку сообщений пользователям которые находятся в сети, сообщения шифруются
с помощью алгоритма RSA с длинной ключа 2048 bit.

Поддерживает аргументы коммандной строки:

``python chat_client.py {имя сервера} {порт} -n или --name {имя пользователя} -p или -password {пароль}``

1. {имя сервера} - адрес сервера сообщений.
2. {порт} - порт по которому принимаются подключения
3. -n или --name - имя пользователя с которым произойдёт вход в систему.
4. -p или --password - пароль пользователя.

Все опции командной строки являются необязательными, но имя пользователя и пароль необходимо использовать в паре.

Примеры использования:

* ``python chat_client.py``

*Запуск приложения с параметрами по умолчанию.*

* ``python chat_client.py ip_address some_port``

*Запуск приложения с указанием подключаться к серверу по адресу ip_address:port*

* ``python chat_client.py -n test1 -p 123``

*Запуск приложения с пользователем test1 и паролем 123*

* ``python chat_client.py ip_address some_port -n test1 -p 123``

*Запуск приложения с пользователем test1 и паролем 123 и указанием подключаться к серверу по адресу ip_address:port*

client.py
~~~~~~~~~~~~~~

Parser for command line arguments, returns a tuple of 4 elements
server address, port, username, password.

Запускаемый модуль,содержит парсер аргументов командной строки и функционал инициализации приложения.

client. **arg_parser** ()
    Парсер аргументов командной строки, возвращает кортеж из 4 элементов:

    * адрес сервера
    * порт
    * имя пользователя
    * пароль

add_contact_window.py
~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: client.add_contact_window.AddContactDialog
    :members:

Client_DataBase.py
~~~~~~~~~~~~~~~~~~

.. autoclass:: client.Client_DataBase.ClientDatabase
    :members:

client_main_window.py
~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: client.client_main_window.ClientMainWindow
    :members:

del_contact_window.py
~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: client.del_contact_window.DelContactDialog
    :members:

start_dialog_window.py
~~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: client.start_dialog_window.UserNameDialog
    :members:

transport.py
~~~~~~~~~~~~

.. autoclass:: client.transport.ClientTransport
    :members:
