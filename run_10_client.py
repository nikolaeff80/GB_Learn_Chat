from _winapi import CREATE_NEW_CONSOLE
from subprocess import Popen

from Log.client_log_config import client_log

p_list = []  # Список клиентских процессов

while True:
    user = input("Запустить 10 клиентов (s) / Закрыть клиентов (x) / Выйти (q) ")
    if user == 'q':
        break
    elif user == 's':
        for _ in range(10):
            p_list.append(Popen('python time_client_random.py', creationflags=CREATE_NEW_CONSOLE))
            client_log.info(f'Список клиентов: {p_list}')
        print(' Запущено 10 клиентов')
    elif user == 'x':
        for p in p_list:
            p.kill()
        p_list.clear()
