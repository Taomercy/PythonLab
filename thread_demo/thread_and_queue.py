import queue
import time
import threading

q = queue.Queue(maxsize=3)


def product(name):
    count = 1
    while True:
        q.put('气球兵{}'.format(count))
        print('{}训练气球兵{}只'.format(name, count))
        count += 1
        time.sleep(1)
        if count > 5:
            print("{} end.".format(name))
            break


def consume(name):
    while True:
        time.sleep(3)
        if not q.empty():
            print('{}使用了{}'.format(name, q.get()))
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
