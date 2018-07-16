import os
import random
import time
from multiprocessing import Process, Queue


def write(q):
    print('process to write %s' % os.getpid())
    for n in ['A', 'B', 'C', ]:
        print("Put %s in Queue" % n)
        q.put(n)
        time.sleep(random.random())


def read(q):
    print('process to read')
    while True:
        value = q.get(True)
        print('Get %s from Queue' % value)


if __name__ == '__main__':
    q = Queue()
    qw = Process(target=write, args=(q,))
    qr = Process(target=read, args=(q,))
    qw.start()
    qr.start()
    qw.join()
    qr.terminate()
    print('Process to END')