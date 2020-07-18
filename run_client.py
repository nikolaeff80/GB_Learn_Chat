"""Программа-лаунчер"""
import logging
import subprocess
from _winapi import CREATE_NEW_CONSOLE

client_log = logging.getLogger('client_log')

process_of_client_list = []

while True:
    process = input("Сколько клиентов запустить? Введите число: \n"
                    "Закрыть все клиенты (x)\n"
                    "Выход (q) ")
    if process != 'q' or 'x':
        for i in range(int(process)):
            process_of_client_list.append(subprocess.Popen(f'python chat_client.py -n test{i}', creationflags=CREATE_NEW_CONSOLE))
            client_log.info(f'Список клиентов: {process_of_client_list}')
            print(f'Запущено {i + 1} клиентов')
            print('')
    elif process == 'q' or 'Q':
        break
    elif process == 'x' or 'X':
        for p in process_of_client_list:
            p.kill()
        process_of_client_list.clear()

# PROCESSES = []
#
# while True:
#     ACTION = input('Выберите действие: q - выход, '
#                    's - запустить сервер и клиенты, '
#                    'x - закрыть все окна: ')
#
#     if ACTION == 'q':
#         break
#     elif ACTION == 's':
#         PROCESSES.append(subprocess.Popen('python chat_server.py', creationflags=subprocess.CREATE_NEW_CONSOLE))
#         PROCESSES.append(subprocess.Popen('python chat_client.py -n test1', creationflags=subprocess.CREATE_NEW_CONSOLE))
#         PROCESSES.append(subprocess.Popen('python chat_client.py -n test2', creationflags=subprocess.CREATE_NEW_CONSOLE))
#         PROCESSES.append(subprocess.Popen('python chat_client.py -n test3', creationflags=subprocess.CREATE_NEW_CONSOLE))
#         LOGGER.info(f'Запущены клиенты и сервер. Список процессов: \n {PROCESSES}')
#     elif ACTION == 'x':
#         while PROCESSES:
#             VICTIM = PROCESSES.pop()
#             VICTIM.kill()
#             LOGGER.info(f'Все клиенты и сервер остановлены')
