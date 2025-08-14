# logger.py
import logging

# Setup logging
logging.basicConfig(filename='trade.log', level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger()

def get_logger():
    return logger
