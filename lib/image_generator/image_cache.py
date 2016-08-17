import sys, os
from PIL import Image
from StringIO import StringIO
import requests
import requests_cache
requests_cache.install_cache('/tmp/lcs_image_cache')

DATA_DRAGON = "http://ddragon.leagueoflegends.com/"

def get_item_image(version, item_num):
    location = _create_item_location(version, item_num)
    return _get_image(location)

def get_champ_image(version, champ_name):
    location = _create_champ_location(version, champ_name)
    return _get_image(location)

def get_summoner_image(version, spell):
    location = _create_sumoner_location(version, spell)
    return _get_image(location)

def _get_image(loc):
    web_loc = _web_location(loc)
    r = requests.get(web_loc, stream=True)
    return Image.open(StringIO(r.content))

def _create_item_location(version, item_num):
    return "cdn/%s/img/item/%s.png" % (version, item_num)

def _create_champ_location(version, champ_name):
    return "cdn/%s/img/champion/%s.png" % (version, champ_name)

def _create_sumoner_location(version, spell):
    return "cdn/%s/img/spell/%s.png" % (version, spell)

def _web_location(loc):
    return os.path.join(DATA_DRAGON, loc)
