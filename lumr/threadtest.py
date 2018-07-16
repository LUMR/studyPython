import threading, multiprocessing
import time
from multiprocessing import Process


def loop():
    x = 0
    while True:
        x = x ^ 1


if __name__ != '__main__':
    for i in range(multiprocessing.cpu_count()):
        t = threading.Thread(target=loop)
        t.start()
        time.sleep(10)

if __name__ == '__main__':
    pl = []
    for i in range(multiprocessing.cpu_count()):
        p = Process(target=loop)
        pl.append(p)
        p.start()
    time.sleep(20)
    for p in pl:
        p.terminate()
