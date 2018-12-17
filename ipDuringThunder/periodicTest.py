import time, threading

def periodic(seconds):
    def periodicRaw():
        threading.Timer(seconds, periodicRaw).start()
        print("time delay: " + str(seconds))

    periodicRaw()

periodic(5)
