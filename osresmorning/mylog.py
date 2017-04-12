import logging
import types
import sys

default = {
    'file': 'temp.log',
    'level': 'INFO'
}

handler = None


def set_config(config):
    global default

    file = config.get('file', default['file'])
    level_s = config.get('level', default['level'])

    if not hasattr(logging, level_s):
        level_s = default['level']

    default = {
        'file': file,
        'level': level_s
    }

    level = getattr(logging, level_s)

    global handler
    handler = logging.FileHandler(file)
    handler.setLevel(level)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)


def get_log(name):
    logger = logging.getLogger(name)
    logger.addHandler(handler)
    logger.setLevel(getattr(logging, default['level']))

    return logger


set_config(default)