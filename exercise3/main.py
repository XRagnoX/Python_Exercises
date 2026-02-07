import threading
import time
from datetime import datetime


counter = 0
INCREMENT = 1000000
LOCK = threading.Lock()

def counter_not_safe():
    global counter
    for _ in range(INCREMENT):
        counter += 1

def counter_thread_safe():

    global counter
    
    with LOCK:
        for _ in range(INCREMENT):
            # time.sleep(0.3)
            # print(f"{counter}")
            counter += 1
    

def start_thread_pool():
    
    t1 = threading.Thread(target=counter_thread_safe)
    t2 = threading.Thread(target=counter_thread_safe)
    
    try:
        t1.start()
        t2.start()
    except KeyboardInterrupt:
        t1.join()
        t2.join()
        print(f"{counter}")
        return
    finally:
        t1.join()
        t2.join()
        print(f"{counter}")
        return
    return

if __name__ == "__main__":
    start_thread_pool()

