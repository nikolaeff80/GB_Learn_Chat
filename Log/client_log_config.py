import logging

client_log = logging.getLogger('client_log')

# create the logging file handler

cfh = logging.FileHandler('client_working.log', encoding='utf-8')

client_log.setLevel(logging.DEBUG)
myFormatter = logging.Formatter('%(asctime)s - %(levelname)s - %(name)s - %(message)s')
cfh.setFormatter(myFormatter)

# add handler to logger object

client_log.addHandler(cfh)
