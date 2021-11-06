from ftplib import FTP
import sys
from logger import Logging

# initializing the Logger class
loggerObject = Logging(
    filename="/home/sarthaknarayan/youtube-dl/logs/logging.log")
logger = loggerObject.logger

HOST = '192.168.1.35'
PORT = 2221

with FTP() as ftp:
    try:
        ftp.connect(host=HOST, port=PORT)
        logger.info("----------------------------")
        logger.info("Connection Successfull")
        ftp.login(user='sarthaknarayan', passwd='789456')
        logger.info("Authentication Successfull")
    except Exception as e:
        logger.info("----------------------------")
        logger.exception(e)
        logger.info("----------------------------")
        logger.info("")
        sys.exit(1)
