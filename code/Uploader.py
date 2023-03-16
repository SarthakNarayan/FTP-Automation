from ftplib import FTP
import sys
from logger import Logging
import argparse
from config import PORT, PASSWORD, USERNAME, IP, LOGGING_LOCATION

parser = argparse.ArgumentParser()
parser.add_argument("--file", type=str, required=True)
args = parser.parse_args()

loggerObject = Logging(filename=LOGGING_LOCATION)
logger = loggerObject.logger

filename = args.file

with FTP() as ftp:
    try:
        ftp.connect(host=IP, port=PORT)
        ftp.login(user=USERNAME, passwd=PASSWORD)

        # assuming that you have directory named podcasts
        # If not then you can create one or provide the name of an existing directory
        ftp.cwd("Podcasts")
        logger.info("Changed Directory to Podcasts, Starting Upload")
        with open(filename, "rb") as file:
            ftp.storbinary(f"STOR {filename}", file)
        logger.info("Upload Completed")
        logger.info("----------------------------")
        logger.info("")
    except Exception as e:
        logger.info("----------------------------")
        logger.exception(e)
        logger.info("----------------------------")
        logger.info("")
        sys.exit(1)
