import logging
import os

from logging.handlers import TimedRotatingFileHandler

server_log = logging.getLogger('server_log')

# create log PATH

PATH = os.path.dirname(os.path.abspath(__file__))
PATH = os.path.join(PATH, 'server_working.log')

# create the logging file handler

sfh = logging.FileHandler(PATH, encoding='utf-8')
Rotate_Handler = TimedRotatingFileHandler(PATH, when='D', interval=1)

server_log.setLevel(logging.DEBUG)
myFormatter = logging.Formatter('%(asctime)s - %(levelname)s - %(name)s - %(message)s')
sfh.setFormatter(myFormatter)

# add handler to logger object

server_log.addHandler(sfh)
server_log.addHandler(Rotate_Handler)
