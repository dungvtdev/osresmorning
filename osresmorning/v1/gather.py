import threading
import time
from .. import mylog as log

from osresmorning import config as base_config


class GatherBot(object):
    _logger = None

    _driver = None
    _pool = None

    _interval = 0
    _time_now = 0

    _backwards_time = 0

    _observer_list = []

    def __init__(self, thread_pool=None):
        self._pool = thread_pool

        self._logger = log.get_log('GatherBot')

        config = base_config.get_config('V1_GATHER')

        self.config_setting(config)

    def config_setting(self, config):
        self._interval = config.get('interval', 60)
        self._backwards_time = config.get('backwards_time', 60)

        self._logger.debug('Setting interval = %d' % self._interval)

        self._driver = base_config.load_module(__name__, 'driver', config['driver'])

    def run_observer(self, observer_data):
        self._logger.debug('Gather data %s' % observer_data)

        self._driver.gather(observer_data)

    def add_observer(self, observer):
        observer['last'] = self._interval

        self._observer_list.append(Observer(data=observer))

        self._logger.debug('Add observer %s' % observer)

    def run(self):
        while True:
            self._logger.debug('Start gather %d component' % len(self._observer_list))

            start_time = time.time()

            # set base time cho observers
            for o in self._observer_list:
                o["base"] = self._time_now

            # gather thread and wait
            for _ in self._pool.imap(self.run_observer, self._observer_list):
                pass

            wait_time = self._interval - (time.time() - start_time)
            wait_time = wait_time if wait_time > 0 else 0

            self._logger.debug('End gather, sleep %f', wait_time)

            time.sleep(wait_time)

            self._time_now += time.time() - self._backwards_time

    def start(self):
        self._time_now = time.time() - self._backwards_time

        t = threading.Thread(target=self.run, args=())
        t.daemon = True
        t.start()

        self._logger.info('Start GatherBot thread with %d component, start_time %f'
                          % (len(self._observer_list), self._time_now))


class Observer(object):
    id = None,
    data = None,

    def __init__(self, data=None):
        self.data = data

    def __str__(self):
        return str(self.data)

    def __getitem__(self, item):
        return self.data[item]

    def __setitem__(self, key, value):
        self.data[key] = value

