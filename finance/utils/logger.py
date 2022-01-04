import logging.handlers

import config

logger = logging.getLogger('finance_log')
logger.setLevel(logging.DEBUG)
fh = logging.handlers.RotatingFileHandler(config.logs_file, mode='a', maxBytes=1000000, backupCount=10)
fh.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
logger.addHandler(fh)
