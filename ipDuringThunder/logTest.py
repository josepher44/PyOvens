#!/usr/bin/python

import requests
import time, threading
import datetime
import logging
import logging.handlers

def initializeLogger():
    log = logging.getLogger(__name__)
    log.setLevel(logging.DEBUG)
    handler = logging.handlers.SysLogHandler(address = '/dev/log')
    formatter = logging.Formatter('%(levelname)s, %(module)s.%(funcName)s: ln %(lineno)d: %(message)s')
    handler.setFormatter(formatter)
    log.addHandler(handler)
    return log

log = initializeLogger()

def getIP(address):
    my_ip = requests.get(address).text
    print(my_ip)

def periodicFunction(seconds, func, f_args):
    threading.Timer(seconds, periodicFunction, args=[seconds, func, f_args]).start()
    func(f_args)
    log.info('This is info')
    log.debug('This is debug')
    log.critical('THIS IS CRITICAL')
    log.info(datetime.datetime.now())

periodicFunction(2, getIP, 'https://api.ipify.org')
