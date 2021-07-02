import logging

logger = logging.getLogger('finance_log')
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler('logs.log')
fh.setLevel(logging.DEBUG)
logger.addHandler(fh)
