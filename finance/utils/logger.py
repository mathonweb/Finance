import logging.handlers
import configparser

config = configparser.ConfigParser()
config.read_file(open('config.ini'))

logger = logging.getLogger('finance_log')
logger.setLevel(logging.DEBUG)
fh = logging.handlers.RotatingFileHandler(config['DEFAULT']['logs_file'], mode='a', maxBytes=1000000, backupCount=10)
fh.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
logger.addHandler(fh)
