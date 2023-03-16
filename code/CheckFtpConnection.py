from ftplib import FTP
import sys
from logger import Logging
from config import USERNAME, PASSWORD, PORT, IP, LOGGING_LOCATION

# initializing the Logger class
loggerObject = Logging(filename=LOGGING_LOCATION)
logger = loggerObject.logger

with FTP() as ftp:
    try:
        ftp.connect(host=IP, port=PORT)
        logger.info("----------------------------")
        logger.info("Connection Successfull")
        ftp.login(user=USERNAME, passwd=PASSWORD)
        logger.info("Authentication Successfull")
    except Exception as e:
        logger.info("----------------------------")
        logger.exception(e)
        logger.info("----------------------------")
        logger.info("")
        sys.exit(1)
