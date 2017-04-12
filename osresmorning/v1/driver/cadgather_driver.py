from eventlet.green import urllib2
import json
from osresmorning import mylog

logger = mylog.get_log("_Data Resources Driver (%s)" % __name__)


def get_data(query_data):
    endpoint = query_data['endpoint']
    user_id = query_data['user_id']
    machine_id = query_data['machine_id']
    metric = query_data['metric']
    last = query_data['last']
    base = query_data['base']

    # get query
    query = 'http://{0}/api/v1/resources_monitoring/users/{1}?'.format(endpoint, user_id)
    query_args = {
        'machine': machine_id,
        'metric': metric,
        'last': last,
    }
    if not base:
        query_args['base'] = base

    endcoded_args = '&'.join(['{0}={1}'.format(k,v) for k,v in query_args.items()])

    url = query + endcoded_args

    req = urllib2.Request(url)
    try:
        resp = urllib2.urlopen(req)
    except Exception as e:
        logger.error('Error when gather data %s' % e.message)
        raise IOError('')

    return resp.read()



def process_data(values):
    mean = reduce(lambda sm, x: sm + x[0], values) / len(values)
    return mean


def write_data(query_data, data):
    print(data)


def gather(query_data):
    try:
        data = get_data(query_data)

    data = json.loads(data)
    data = getattr(data, "data", None)

    if not data:
        logger.warn('Query data %s result None' % query_data)

    ls = []
    for measurement, it in data.items():
        if not it["data"]:
            logger.warn('Query data %s return Empty data, container %s'
                        % (query_data, getattr(it, "container", None)))
            break

        values = it["data"]["values"]
        if not values:
            logger.warn('Query data %s return Empty data, container %s'
                        % (query_data, getattr(it, "container", None)))

        mean = process_data(values)
        t = (values[0][0] + values[len(values) - 1][0]) / 2.0

        s = "{0} value={1} {2}".format(measurement, mean, t)
        ls.append(s)

    data_to_write = '\n'.join(ls)

    write_data(query_data, data_to_write)
