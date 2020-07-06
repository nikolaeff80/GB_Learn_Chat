import logging
import os

client_log = logging.getLogger('client_log')

# create log PATH

PATH = os.path.dirname(os.path.abspath(__file__))
PATH = os.path.join(PATH, 'client_working.log')

# create the logging file handler

cfh = logging.FileHandler(PATH, encoding='utf-8')

client_log.setLevel(logging.DEBUG)
myFormatter = logging.Formatter('%(asctime)s - %(levelname)s - %(name)s - %(message)s')
cfh.setFormatter(myFormatter)

# add handler to logger object

client_log.addHandler(cfh)
