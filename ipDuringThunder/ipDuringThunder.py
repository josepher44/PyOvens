import requests
import time, threading

def getIP(address):
    my_ip = requests.get(address).text

    print(my_ip)

def periodicFunction(seconds, func, f_args):
    threading.Timer(seconds, periodicFunction, args=[seconds, func, f_args]).start()
    func(f_args)

periodicFunction(2, getIP, 'https://api.ipify.org')
