import queue
import time
import threading

q = queue.Queue(maxsize=3)


def product(name):
    count = 1
    while True:
        q.put('cake {}'.format(count))
        print('{} create cake {}'.format(name, count))
        count += 1
        time.sleep(1)
        if count > 7:
            print("{} end.".format(name))
            break


def consume(name):
    time.sleep(3)
    while True:
        if not q.empty():
            print('{} eat {}'.format(name, q.get()))
            time.sleep(5)
            q.task_done()
        else:
            print("{} end.".format(name))
            break


t1 = threading.Thread(target=product, args=('product',))
t2 = threading.Thread(target=consume, args=('consume',))
t3 = threading.Thread(target=consume, args=('others',))

t1.start()
t2.start()
t3.start()
