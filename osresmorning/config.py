import sys


def apply_all_config(config_module):
    keys = dir(config_module)
    for k in keys:
        if k[:2] == '__' or type(getattr(config_module, k, None)) == 'function':
            continue

        apply_config(k, getattr(config_module, k, None))


def apply_config(key, config):
    if not config:
        return

    md = sys.modules[__name__]
    base_config = getattr(md, key, None)

    if not base_config:
        return

    if key[:2] == '__' or type(base_config) == 'function':
        raise KeyError('Config with key %s not invalid' % key)

    for k, it in config.items():
        base_config[k] = it


def get_config(key):
    md = sys.modules[__name__]
    return getattr(md, key, None)


def load_module(caller, folder, name):
    path = '.'.join(caller.split('.')[:-1]) if caller else ''
    path = '{0}.{1}.{2}'.format(path, folder, name)

    md = __import__(path, globals(), locals(), ['object'], -1)

    return md


APP = {
    'pool_size': 1000
}

LOG = {
    'file': 'temp.log',
    'level': 'INFO'
}

V1_HANDLER = {

}

V1_GATHER = {
    'interval': 60,
    'backwards_time': 30,
    'driver': 'cadgather_driver'
}
