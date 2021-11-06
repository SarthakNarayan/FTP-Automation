from ftplib import FTP
import sys
from logger import Logging
import argparse
import os

parser = argparse.ArgumentParser()
parser.add_argument('--file', type=str, required=True)
args = parser.parse_args()

loggerObject = Logging(
    filename="/home/sarthaknarayan/youtube-dl/logs/logging.log")
logger = loggerObject.logger

HOST = '192.168.1.35'
PORT = 2221
# absolute path didn't work for me
# filename = os.path.join('/home/sarthaknarayan/youtube-dl', args.file)
filename = args.file

with FTP() as ftp:
    try:
        ftp.connect(host=HOST, port=PORT)
        ftp.login(user='sarthaknarayan', passwd='789456')
        ftp.cwd('Podcasts')
        logger.info("Changed Directory to Podcasts, Starting Upload")
        with open(filename, "rb") as file:
            ftp.storbinary(f'STOR {filename}', file)
        logger.info("Upload Completed")
        logger.info("----------------------------")
        logger.info("")
    except Exception as e:
        logger.info("----------------------------")
        logger.exception(e)
        logger.info("----------------------------")
        logger.info("")
        sys.exit(1)
