#ntlogging.py
import logging
from logging.handlers import RotatingFileHandler

# levels: CRITICAL ERROR WARNING INFO DEBUG NOTSET
logging.basicConfig(
    level=logging.INFO,  # minimum level capture in the FILE
    #format='[%(asctime)s] %(levelname)s: %(message)s',
    format='%(levelname)s: %(message)s',
    datefmt='%m/%d/%Y %I:%M:%S %p',
    handlers=[
        RotatingFileHandler("{0}/{1}.log".format(".", "log-gkg"), mode='a', 
            maxBytes=1048576),
        logging.StreamHandler()]
    )
