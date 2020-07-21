"""Программа-лаунчер"""
import logging
import subprocess

client_log = logging.getLogger('client_log')

process_of_client_list = []

while True:
    process = input("Сколько клиентов запустить? Введите число: \n"
                    "Закрыть все клиенты (x)\n"
                    "Выход (q) ")
    if process.isdigit():
        for i in range(int(process)):
            process_of_client_list.append(subprocess.Popen(f'python chat_client.py -n test{i}', creationflags=subprocess.CREATE_NEW_CONSOLE))
            client_log.info(f'Список клиентов: {process_of_client_list}')
            print(f'Запущено {i + 1} клиентов')
            print('')
    elif process == 'q' or 'Q':
        break
    elif process == 'x' or 'X':
        while process_of_client_list:
            VICTIM = process_of_client_list.pop()
            VICTIM.kill()
            client_log.info(f'Все клиенты и сервер остановлены')

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
#         client_log.info(f'Запущены клиенты и сервер. Список процессов: \n {PROCESSES}')
#     elif ACTION == 'x':
#         while PROCESSES:
#             VICTIM = PROCESSES.pop()
#             VICTIM.kill()
#             client_log.info(f'Все клиенты и сервер остановлены')
