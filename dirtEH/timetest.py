import time, threading
def foo():
    print("time")
    print(time.ctime())
    threading.Timer(10, foo).start()

foo()
