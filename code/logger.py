import logging
from logging.handlers import RotatingFileHandler


class Logging:
    def __init__(self, filename) -> None:
        self.logger = logging.getLogger()
        self.formatter = logging.Formatter(
            '[%(asctime)s] - [%(levelname)s] - [%(message)s]')
        self.logger.setLevel(logging.DEBUG)
        self.filename = filename
        self.LoggerSetup()

    def LoggerSetup(self):
        self.InfoFileHandlerSetup()
        # self.StreamHandlerSetup()
        # self.RotatingFileHandlerSetup()

    def InfoFileHandlerSetup(self):
        fileHandlerInfo = logging.FileHandler(self.filename)
        fileHandlerInfo.setFormatter(self.formatter)
        fileHandlerInfo.setLevel(logging.INFO)
        self.logger.addHandler(fileHandlerInfo)

    def StreamHandlerSetup(self):
        streamHandler = logging.StreamHandler()
        streamHandler.setFormatter(self.formatter)
        streamHandler.setLevel(logging.DEBUG)
        self.logger.addHandler(streamHandler)

    def RotatingFileHandlerSetup(self):
        rotatingHandler = RotatingFileHandler(self.filename,
                                              maxBytes=20,
                                              backupCount=5)
        rotatingHandler.setFormatter(self.formatter)
        rotatingHandler.setLevel(logging.DEBUG)
        self.logger.addHandler(rotatingHandler)
