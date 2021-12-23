import stopit
import time


@stopit.threading_timeoutable(False, timeout_param="timeout")
def loop():
    for i in range(10):
        print(i)
        time.sleep(3)
    return True


print(loop(timeout=6))
