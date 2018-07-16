import asyncio
import threading


@asyncio.coroutine
def hello():
    print('hello thread:%s' % threading.currentThread())
    yield from asyncio.sleep(1)
    print("hello again thead:%s" % threading.currentThread())


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    tasks = [hello(), hello()]
    loop.run_until_complete(asyncio.wait(tasks))
    print("loot run")
    loop.close()
