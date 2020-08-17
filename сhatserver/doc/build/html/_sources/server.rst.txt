Server module
=================================================

Серверный модуль мессенджера. Обрабатывает словари - сообщения, хранит публичные ключи клиентов.

Использование

Модуль подерживает аргементы командной стороки:

1. -p - Порт на котором принимаются соединения
2. -a - Адрес с которого принимаются соединения.
3. --no_gui Запуск только основных функций, без графической оболочки.

* В данном режиме поддерживается только 1 команда: exit - завершение работы.

Примеры использования:

``python chat_server.py -p 8080``

*Запуск сервера на порту 8080*

``python server.py -a localhost``

*Запуск сервера принимающего только соединения с localhost*

``python server.py --no-gui``

*Запуск без графической оболочки*

server.py
~~~~~~~~~~~~~~

Запускаемый модуль,содержит парсер аргументов командной строки и функционал инициализации приложения.

server. **arg_parser** ()
    Парсер аргументов командной строки, возвращает кортеж из 4 элементов:

    * адрес с которого принимать соединения
    * порт
    * флаг запуска GUI

server. **config_load** ()
    Функция загрузки параметров конфигурации из ini файла.
    В случае отсутствия файла задаются параметры по умолчанию.

add_user_window.py
~~~~~~~~~~~~~~~~~~

.. autoclass:: server.add_user_window.RegisterUser
   :members:

main_window.py
~~~~~~~~~~~~~~

.. autoclass:: server.main_window.MainWindow
   :members:

remove_user_window.py
~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: server.remove_user_window.DelUserDialog
   :members:

server_conf_window.py
~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: server.server_conf_window.ConfigWindow
   :members:

server_core.py
~~~~~~~~~~~~~~

.. autoclass:: server.server_core.MessageProcessor
   :members:

Server_DataBase.py
~~~~~~~~~~~~~~~~~~

.. autoclass:: server.Server_DataBase.ServerDB
   :members:

stat_window.py
~~~~~~~~~~~~~~~~

.. autoclass:: server.stat_window.StatWindow
   :members:
