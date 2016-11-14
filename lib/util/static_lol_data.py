import os
from PIL import Image
try:
    from StringIO import StringIO as inIO
except ImportError:
    from io import BytesIO as inIO
import requests
import requests_cache

from lib.util.static_vals import CACHE_DIR

DATA_DRAGON = "http://ddragon.leagueoflegends.com/"
STATIC_CACHE = 'lcs_static_cache'


def get_item_image(version, item_num):
    location = _create_item_location(version, item_num)
    return _get_image(location)


def get_champ_image(version, champ_name):
    if is_number(champ_name):
        champ_name = lookup_champ_name(version, champ_name)
    location = _create_champ_location(version, champ_name)
    return _get_image(location)


def get_champ_data(version, champ_name):
    if is_number(champ_name):
        champ_name = lookup_champ_name(version, champ_name)
    location = _create_champion_data_location(version)
    data = _get_data(location)
    return data['data'][champ_name]['stats']


def get_summoner_image(version, spell):
    if is_number(spell):
        spell = lookup_summoner_name(version, spell)
    location = _create_summoner_location(version, spell)
    return _get_image(location)


def get_icon_image(version, icon):
    location = _create_icon_location(version, icon)
    return _get_image(location)


def _request(url):
    with requests_cache.enabled(os.path.join(CACHE_DIR, STATIC_CACHE)):
        return requests.get(url, stream=True)


def _get_image(loc):
    web_loc = _web_location(loc)
    r = _request(web_loc)
    try:
        return Image.open(inIO(r.content))
    except IOError as e:
        raise e


def _get_data(loc):
    web_loc = _web_location(loc)
    r = _request(web_loc)
    try:
        return r.json()
    except IOError as e:
        raise e


def _lookup_resource_name(url, id_val):
    data = _request(url)
    data = data.json()
    for key, data in data['data'].iteritems():
        if int(data['key']) == int(id_val):
            return key


def _create_item_location(version, item_num):
    return "cdn/%s/img/item/%s.png" % (version, item_num)


def _create_champ_location(version, champ_name):
    return "cdn/%s/img/champion/%s.png" % (version, champ_name)


def _create_summoner_location(version, spell):
    return "cdn/%s/img/spell/%s.png" % (version, spell)


def _create_icon_location(version, icon):
    return "cdn/%s/img/ui/%s.png" % (version, icon)


def _create_champion_data_location(version):
    return "cdn/%s/data/en_US/champion.json" % version


def _create_summoner_data_location(version):
    return "cdn/%s/data/en_US/summoner.json" % version


def _web_location(loc):
    return os.path.join(DATA_DRAGON, loc)


def lookup_champ_name(version, champ_id):
    return _lookup_resource_name(_web_location(_create_champion_data_location(version)), champ_id)


def lookup_summoner_name(version, summoner_id):
    return _lookup_resource_name(_web_location(_create_summoner_data_location(version)), summoner_id)


def is_number(s):
    try:
        int(s)
        return True
    except ValueError:
        return False


if __name__ == "__main__":
    #get_champ_image("6.18.1", 143).show()
    print get_champ_data("6.22.1", "Aatrox")
