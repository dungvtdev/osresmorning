import requests
import json
from osresmorning import mylog

__all__ = ['gather']

logger = mylog.get_log("_Data Resources Driver (%s)" % __name__)


def get_data(query_data):
    endpoint = query_data['endpoint']
    user_id = query_data['user_id']
    machine_id = query_data['machine_id']
    metric = query_data['metric']
    last = query_data['last']
    base = query_data['base']

    # get query
    query = 'http://{0}/api/v1/resources_monitoring/users/{1}'.format(endpoint, user_id)
    query_args = {
        'machine': machine_id,
        'metric': metric,
        'last': "{0}s".format(last),
    }
    if base:
        query_args['base'] = "%ds" % base

    # endcoded_args = '&'.join(['{0}={1}'.format(k,v) for k,v in query_args.items()])

    r = requests.get(query, params=query_args)
    print(r.url)
    # print(r.text)
    if r.status_code != 200:
        raise IOError('Query error')
    else:
        return r.text


def process_data(values):
    mean = sum(v[1] for v in values) / len(values)
    return mean


def write_data(query_data, data):
    print(data)


def gather(query_data):
    try:
        data = get_data(query_data)
    except Exception as e:
        logger.error("Query data exception {0}, error: {1}".format(query_data, e.message))
        return

    print(data)
    data = json.loads(data)
    data = data.get("data", None)

    if not data:
        logger.warn('Query data result None %s' % query_data)

    ls = []
    for measurement, it in data.items():
        if not it["data"]:
            logger.warn('Query data return Empty data, container %s %s'
                        % (it.get("container", None), query_data))
            break

        values = it["data"][0]["values"]
        if not values:
            logger.warn('Query data return Empty data, container %s %s'
                        % (it.get("container", None), query_data))

        mean = process_data(values)
        t = (values[0][0] + values[len(values) - 1][0]) / 2.0

        s = "{0} value={1} {2}".format(measurement, mean, t)
        ls.append(s)

    data_to_write = '\n'.join(ls)

    write_data(query_data, data_to_write)
