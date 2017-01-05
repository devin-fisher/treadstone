import os
import requests
import requests_cache
import time
from collections import OrderedDict

from lib.util.static_vals import CACHE_DIR

LOCAL_HOST = '127.0.0.1'
LOCAL_PORT = '80' if str(__file__).startswith("/opt/treadstone") else '8555'

URL_FORMAT = 'http://%s:%s/%s'


def request_json_resource(url, retry=3, time_between=1):
    with requests_cache.enabled(os.path.join(CACHE_DIR, 'lcs_static_cache')):
        for i in range(retry):
            response = requests.get(url, headers={'Origin': 'http://www.lolesports.com'})
            if response.status_code == 200:
                return response.json(object_pairs_hook=OrderedDict)
            elif response.status_code == 404:
                break
            else:
                time.sleep(time_between)

        raise Exception('Unable to retrieve json recourse')


def request_json_resource_cacheless(url, retry=3, time_between=1):
    with requests_cache.disabled():
        for i in range(retry):
            response = requests.get(url, headers={'Origin':'http://www.lolesports.com'})
            if response.status_code == 200:
                return response.json(object_pairs_hook=OrderedDict)
            elif response.status_code == 404:
                break
            else:
                time.sleep(time_between)

        raise Exception('Unable to retrieve json recourse')


def request_api_resource(relative_url, retry=3, time_between=1):
    url = URL_FORMAT % (LOCAL_HOST, LOCAL_PORT, relative_url)
    with requests_cache.disabled():
        for i in xrange(retry):
            response = requests.get(url)
            if response.status_code == 200:
                return response.json(object_pairs_hook=OrderedDict)
            elif response.status_code == 404:
                raise Exception('Bracket Info is Invalid, 404 when retrieving bracket data')
            else:
                time.sleep(time_between)

        raise Exception('Unable to retrieve json recourse')
