import logging

from logging.handlers import TimedRotatingFileHandler

server_log = logging.getLogger('server_log')

# create the logging file handler

sfh = logging.FileHandler('server_working.log', encoding='utf-8')
Rotate_Handler = TimedRotatingFileHandler('server_working.log', when='D', interval=1)

server_log.setLevel(logging.DEBUG)
myFormatter = logging.Formatter('%(asctime)s - %(levelname)s - %(name)s - %(message)s')
sfh.setFormatter(myFormatter)


# add handler to logger object

server_log.addHandler(sfh)
server_log.addHandler(Rotate_Handler)



