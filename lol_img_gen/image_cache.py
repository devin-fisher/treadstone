import sys, os
from PIL import Image
import requests

DISK_CACHE_LOCATION = "/var/cache/lol_image_image/"
DATA_DRAGON = "http://ddragon.leagueoflegends.com/"

def get_item_image(version, item_num):
    location = _create_item_location(version, item_num)
    return _get_image(location)

def get_champ_image(version, champ_name):
    location = _create_champ_location(version, champ_name)
    return _get_image(location)

def _get_image(loc):
    if not _is_on_disk(loc):
        _download_image(loc)

    return _load_from_disk(loc)

def _create_item_location(version, item_num):
    return "cdn/%s/img/item/%s.png" % (version, item_num)

def _create_champ_location(version, champ_name):
    return "cdn/%s/img/champion/%s.png" % (version, champ_name)

def _load_from_disk(loc):
    disk_loc = _disk_location(loc)
    return Image.open(disk_loc)

def _is_on_disk(loc):
    return os.path.isfile(_disk_location(loc))

def _web_location(loc):
    return os.path.join(DATA_DRAGON, loc)

def _disk_location(loc):
    return os.path.join(DISK_CACHE_LOCATION, loc)

def _download_image(loc):
    web_loc = _web_location(loc)
    disk_loc = _disk_location(loc)
    _make_dir_if_needed(disk_loc)
    r = requests.get(web_loc, stream=True)
    if r.status_code == 200:
        with open(disk_loc, 'wb') as f:
            for chunk in r:
                f.write(chunk)

def _make_dir_if_needed(loc):
    file_dir = os.path.dirname(loc)
    if not os.path.isdir(file_dir):
        os.makedirs(os.path.dirname(loc))
