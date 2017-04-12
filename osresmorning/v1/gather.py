import threading
import time
from .. import mylog as log

from osresmorning import config as base_config

class GatherBot(object):
    _logger = None

    _pool = None
    _interval = 0

    _observer_list = []

    def __init__(self, thread_pool=None, config=None):
        self._pool = thread_pool

        self._logger = log.get_log('GatherBot')

        config = config if config is not None else base_config.get_config('V1_GATHER')

        self.config_setting(config)

    def config_setting(self, config):
        self._interval = config.get('interval', 60)

        self._logger.debug('Setting interval = %d' % self._interval)

    def run_observer(self, observer_data):
        self._logger.debug('Gather data %d' % observer_data.id)

    def add_observer(self, observer):
        if observer.id not in [o.id for o in self._observer_list]:
            self._observer_list.append(observer)

            self._logger.debug('Add observer id %s' % observer)

    def run(self):
        while True:
            self._logger.debug('Start gather %d component' % len(self._observer_list))

            start_time = time.time()

            for result in self._pool.imap(self.run_observer, self._observer_list):
                pass

            wait_time = self._interval - (time.time() - start_time)
            wait_time = wait_time if wait_time > 0 else 0

            self._logger.debug('End gather, sleep %d', wait_time)

            time.sleep(wait_time)

    def start(self):
        t = threading.Thread(target=self.run, args=())
        t.daemon = True
        t.start()

        self._logger.info('Start GatherBot thread with %d component' % len(self._observer_list))


class Observer(object):
    id = None,
    data = None,

    def __init__(self, id=None, data=None):
        self.id = id
        self.data = data