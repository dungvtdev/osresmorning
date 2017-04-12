import eventlet
import threading
import time

class GatherBot(object):
    _pool = None
    _interval = 0

    _observer_list = []

    def __init__(self, thread_pool=None, config=None):
        self._pool = thread_pool
        self.config_setting(config)

    def config_setting(self, config):
        self._interval = config.get('interval', 60)

    def run_observer(self, observer_data):
        pass

    def run(self):
        while True:
            start_time = time.time()

            for result in self._pool.imap(self.run_observer, self._observer_list):
                pass

            run_time = time.time() - start_time
            run_time = run_time if run_time>0 else 0

            time.sleep(run_time)

    def start(self):
        t = threading.Thread(target=self.run, args=())
        t.daemon = True
        t.start()