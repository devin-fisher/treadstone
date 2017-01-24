from lib.util.http_lol_static import request_json_resource_cacheless
import string
from dateutil.parser import parse
from datetime import timedelta
import re

DEFAULT_PARAMETERS = {
    'part': 'id,snippet',
    'type': 'video',
    'key': 'AIzaSyDV3vsGVOBXP4BTL4N-10HvSq0QkKDIONs',
    'order': 'date',
    'channelId': 'UCdOWyp25T0HDtjpnV2LpIyw'
}
GOOGLE_YOUTUBE_SEARCH = 'https://www.googleapis.com/youtube/v3/search'
FIND_PUNCTUATION = re.compile('[%s]' % re.escape(string.punctuation))


def _convert_data(datatime_obj):
    rtn = datatime_obj.isoformat("T")
    rtn = rtn[:rtn.rfind("+")] + "Z"
    return rtn


def find_youtube_url(game_id, game_data, game_analysis, client):
    epic_link = look_for_epicquickshot(
        game_analysis.get('match_name', None),
        game_analysis.get('game_name', None),
        game_analysis.get('match_scheduled_time', None))
    if epic_link:
        return epic_link
    return game_data.get('youtube_url', None)


def look_for_epicquickshot(match_name, game_name, game_scheduled_time):
    if not match_name or not game_name or not game_scheduled_time:
        return None

    params = dict(DEFAULT_PARAMETERS)

    match_name = FIND_PUNCTUATION.sub(' ', match_name)
    params['q'] = match_name + " " + game_name
    if game_scheduled_time:
        scheduled = parse(game_scheduled_time)
        after = scheduled - timedelta(days=2)
        before = scheduled + timedelta(days=2)
        params['publishedAfter'] = _convert_data(after)
        params['publishedBefore'] = _convert_data(before)

    search_list = request_json_resource_cacheless(GOOGLE_YOUTUBE_SEARCH, params=params)
    items = search_list.get('items', None)
    if items and 'id' in items[0] and 'videoId' in items[0]['id']:
        youtube_id = items[0]['id']['videoId']
        return 'https://www.youtube.com/watch?v=' + youtube_id
    return None


if __name__ == "__main__":
    print look_for_epicquickshot('TSM-vs-IMT', "G1", "2017-01-22T20:00:00.000+0000")
    pass
