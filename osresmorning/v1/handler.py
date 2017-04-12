import falcon
from osresmorning import config as base_config

def set_config(config):
    pass

app = application = falcon.API()

# config
config = base_config.get_config('V1_HANDLER')
set_config(config)