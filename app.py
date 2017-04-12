import config
from osresmorning import config as base_config

# config
base_config.apply_all_config(config)

import eventlet

from osresmorning.v1 import handler as handler_v1
from osresmorning.v1 import gather



# init falcon
app = application = handler_v1.app

# init gather bot
app_config = base_config.get_config('APP')

pool = eventlet.GreenPool(app_config['pool_size'])

gather_bot = gather.GatherBot(pool)
gather_bot.start()