import threading
import time

def run():
    while True:
        print('test')
        time.sleep(1)

t = threading.Thread(target=run, args=())
t.daemon = False
t.start()