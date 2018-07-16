
# 分布式队列

import time, queue
from multiprocessing.managers import BaseManager


class QueueManager(BaseManager):
    pass


QueueManager.register('get_task_queue')
QueueManager.register('get_result_queue')

address_str = 'localhost'
print('Connect to server %s...' % address_str)
manager = QueueManager(address=(address_str, 5000), authkey=b'abc')
manager.connect()
task = manager.get_task_queue()
result = manager.get_result_queue()
for i in range(10):
    try:
        n = task.get(timeout=1)
        print('run task %d * %d...' % (n, n))
        r = '%d * %d = %d' % (n, n, n * n)
        time.sleep(1)
        result.put(r)
    except queue.Queue.Empty:
        print('task queue is empty.')
# 处理结束:
print('worker exit.')
