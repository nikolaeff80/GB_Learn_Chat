# GB_Learn_Chat
Network chat development in the learning process in Geek University Python-dev

LAUNCHER.PY

Модуль запуска нескольких тестовых клиентов одновременно.

После запуска будет выведено приглашение ввести команду. Поддерживаемые команды:

s - Запустить сервер

Запускает сервер с настройками по умолчанию.

k - Запустить клиенты

Будет выведен запрос на количество тестовых клиентов для запуска.

Клиенты будут запущены с именами вида test1 - testX и паролями 123

Тестовых пользователей необходимо предварительно, вручную зарегистрировать на сервере с паролем 123.

Если клиенты запускаются впервые, время запуска может быть достаточно продолжительным из-за генерации новых RSA ключей.

x - Закрыть все окна

Закрывает все активные окна, которые были запущенны из данного модуля.

q - Завершить работу модуля

Завершает работу модуля

CLIENT.PY

Клиентское приложение для обмена сообщениями. Поддерживает отправку сообщений пользователям которые находятся в сети, сообщения шифруются с помощью алгоритма RSA с длинной ключа 2048 bit.

Поддерживает аргументы командной строки:

python client.py {имя сервера} {порт} -n или --name {имя пользователя} -p или -password {пароль}

{имя сервера} - адрес сервера сообщений.

{порт} - порт по которому принимаются подключения

-n или –name - имя пользователя с которым произойдёт вход в систему.

-p или –password - пароль пользователя.

Все опции командной строки являются необязательными, но имя пользователя и пароль необходимо использовать в паре.

Примеры использования:

python client.py

Запуск приложения с параметрами по умолчанию.

python client.py ip_address some_port

Запуск приложения с указанием подключаться к серверу по адресу ip_address:port

python -n test1 -p 123

Запуск приложения с пользователем test1 и паролем 123

python client.py ip_address some_port -n test1 -p 123

Запуск приложения с пользователем test1 и паролем 123456 и указанием подключаться к серверу по адресу ip_address:port


SERVER.PY

Серверный модуль мессенджера. Обрабатывает словари - сообщения, хранит публичные ключи клиентов.

Использование

Модуль подерживает аргументы командной стороки:

-p - Порт на котором принимаются соединения

-a - Адрес с которого принимаются соединения.

–no_gui Запуск только основных функций, без графической оболочки.

В данном режиме поддерживается только 1 команда: exit - завершение работы.


Примеры использования:

python server.py -p 8080

Запуск сервера на порту 8080

python server.py -a localhost

Запуск сервера принимающего только соединения с localhost

python server.py --no-gui

Запуск без графической оболочки
