import config
from osresmorning import config as base_config

# config
base_config.apply_all_config(config)

from osresmorning import mylog
mylog.get_log(__name__).info('***************************************************'
                             '***    Start new session    ***'
                             '***************************************************')

import eventlet

from osresmorning.v1 import handler as handler_v1
from osresmorning.v1 import gather




# init falcon
app = application = handler_v1.app

# init gather bot
app_config = base_config.get_config('APP')

pool = eventlet.GreenPool(app_config['pool_size'])

gather_bot = gather.GatherBot(pool)

# test
observer = {
    'endpoint': '192.168.1.226:8090',
    'user_id': 1,
    'machine_id':1,
    'metric': 'cpu_usage_total./,rx_bytes',
}

gather_bot.add_observer(observer)

gather_bot.start()