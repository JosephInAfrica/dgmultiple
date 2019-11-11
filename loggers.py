#!encoding=utf-8
from setting import setting
import logging
import os

vformatter = logging.Formatter(
    '%(message)s')

regularformatter = logging.Formatter(
    '%(asctime)s %(message)s', datefmt='%m/%d/ %I:%M')


def createLogger(logFile, formatterF):
    if not os.path.exists(setting.logsdir):
        os.mkdir(setting.logsdir)

    if not os.path.exists(logFile):
        open(logFile, 'a').close()

    logger = logging.getLogger(logFile)
    logger.setLevel(logging.WARNING)
    fileHandler = logging.handlers.RotatingFileHandler(
        logFile, mode="a", maxBytes=5 * 1024 * 1024, backupCount=2)

    fileHandler.setFormatter(formatterF)
    logger.addHandler(fileHandler)
    return logger

rlogger = createLogger(setting.regular_log, regularformatter)
elogger = createLogger(setting.error_log, regularformatter)


def rlog(message):
    rlogger.warning(message)
    try:
        os.system('sync')
    except Exception as e:
        print(e)


def elog(message):
    elogger.exception(message)
    try:
        os.system("sync")
    except Exception as e:
        pass
