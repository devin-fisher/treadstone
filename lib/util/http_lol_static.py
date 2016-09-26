import requests
import requests_cache
import time
from collections import OrderedDict

# requests_cache.install_cache('/tmp/lcs_static_cache')


def request_json_resource(url, retry=3, time_between=1):
    for i in range(retry):
        response = requests.get(url, headers={'Origin':'http://www.lolesports.com'})
        if response.status_code == 200:
            return response.json(object_pairs_hook=OrderedDict)
        elif response.status_code == 404:
            break
        else:
            time.sleep(time_between)

    raise Exception('Unable to retrieve json recourse')
