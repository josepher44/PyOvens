#!/usr/bin/python

import requests
import time, threading
import datetime
import logging
import logger
import re
import os

log = logger.initializeLogger()
database_ip = "invalid"


def databaseInit():
    #Read ip from database, creating new database if it does not exist
    try:
        file = open("/var/log/netscripts/netdata","r+")
        dbip = file.readline()
    except IOError:
        print("Could not reliably determine last IP. First API call will be assumed"+
        "as current")
        print("Attempting to create new file")
        try:
            file = open("/var/log/netscripts/netdata","w+")
            print("New database file successfully created")
            os.chmod("/var/log/netscripts/netdata", 0777)
            file = open("/var/log/netscripts/netdata","r+")
        except:
            print("Something has gone very wrong. Check permissions")
    return (file, dbip)

def getIP(address):
    global database_ip
    current_ip = requests.get(address).text
    print(current_ip)
    if current_ip != database_ip:
        print("IP mismatch detected, script beginning...")
        print(database_ip)
        file.seek(0)
        file.write(current_ip)
        file.truncate()
        database_ip = current_ip
        print("Wrote new IP to database")



def periodicFunction(seconds, func, f_args):
    threading.Timer(seconds, periodicFunction, args=[seconds, func, f_args]).start()
    func(f_args)
    log.info('This is info')
    log.debug('This is debug')
    log.critical('THIS IS CRITICAL')
    log.info(datetime.datetime.now())

databaseReturn = databaseInit()
database_ip = databaseReturn[1]
file = databaseReturn[0]

print(database_ip)

pattern = re.compile("^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$")
if pattern.match(database_ip):
    print("Valid IP format")
else:
    print("Invalid IP format")

periodicFunction(2, getIP, 'https://api.ipify.org')
