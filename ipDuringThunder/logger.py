#!/usr/bin/python
import logging.handlers

def initializeLogger():
    log = logging.getLogger(__name__)
    log.setLevel(logging.DEBUG)
    handler = logging.handlers.SysLogHandler(address = '/dev/log')
    handle2 = logging.FileHandler('pylog.log')
    formatter = logging.Formatter('%(levelname)s, %(module)s.%(funcName)s: ln %(lineno)d: %(message)s')
    handler.setFormatter(formatter)
    handle2.setFormatter(formatter)
    log.addHandler(handler)
    log.addHandler(handle2)
    return log
