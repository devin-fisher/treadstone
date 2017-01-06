import time

from lib.game_analysis.video_dowload import YoutubeFile
from lib.timeline_analysis.events import report as timeline_events
from lib.timeline_analysis.infographic import infographic_list_builder as timeline_infographic
from lib.video.video_analysis import standard_analysis as video_analysis
from lib.timeline_analysis.video_cooralator import video_event_translator
from lib.util.mongo_util import mongodb_id_convert
from lib.util.http_lol_static import request_api_resource, request_json_resource_cacheless

BRACKET_DATA_URL = "api/leagues/%(league)s/tournaments/%(tournament_id)s/brackets/%(bracket_id)s"


def played_game(game_data):
    if game_data.get('gameId', None):
        return True

    return False


def save_game_analysis(game_id, game_analysis, client, error_msg=None):
    coll = client.lol.game_analysis
    if '_id' not in game_analysis:
        game_analysis['_id'] = mongodb_id_convert(game_id)

    if error_msg:
        error_list = game_analysis.get('error_msg', list())
        if not isinstance(error_list, list):
            error_list = list({'unknown', str(error_list)})
        error_list.append(error_msg)
        game_analysis['error_msg'] = error_list

    game_analysis['time_stamp'] = int(time.time())

    coll.save(game_analysis)


def get_game_length(stats_url):
    if stats_url is None:
        raise Exception("Stats URL for game was not defined")

    stats_data = request_json_resource_cacheless(stats_url)
    length = stats_data.get('gameDuration', None)
    if length is None:
        raise Exception("Was unable to get Game Length from stats file")
    return length


def _timeline_analysis(func, key_val, game_id, game_data, game_analysis, client):
    if key_val in game_analysis:
        return game_analysis

    timeline_url = game_data.get('timeline_url', None)
    stats_url = game_data.get('stats_url', None)
    if timeline_url is None or stats_url is None:
        raise Exception("Time Line URL is not defined")

    game_analysis[key_val] = func(timeline_url, stats_url)
    save_game_analysis(game_id, game_analysis, client)

    return game_analysis


def do_timeline_event_analysis(game_id, game_data, game_analysis, client):
    _timeline_analysis(timeline_events, 'time_line_events', game_id, game_data, game_analysis, client)


def do_timeline_infographic_analysis(game_id, game_data, game_analysis, client):
    _timeline_analysis(timeline_infographic, 'time_line_infographic', game_id, game_data, game_analysis, client)


def do_timeline_video_analysis(game_id, game_data, game_analysis, client):
    key_val = 'video_analysis'
    if key_val in game_analysis:
        return game_analysis

    timeline_url = game_data.get('timeline_url', None)
    stats_url = game_data.get('stats_url', None)
    if timeline_url is None or stats_url is None:
        raise Exception("Time Line URL is not defined")

    length = get_game_length(game_data.get('stats_url', None))
    youtube_url = game_data.get('youtube_url', None)

    with YoutubeFile(youtube_url, game_id) as video_path:
        analysis = video_analysis(video_path, length, verbose=True)

    # print analysis
    game_analysis[key_val] = analysis
    game_analysis['youtube_url'] = youtube_url
    save_game_analysis(game_id, game_analysis, client)


def do_timeline_video_translation(game_id, game_data, game_analysis, client):
    key_val = 'event_translation'
    if key_val in game_analysis:
        return game_analysis

    timeline_url = game_data.get('timeline_url', None)
    stats_url = game_data.get('stats_url', None)
    if timeline_url is None or stats_url is None:
        raise Exception("Time Line URL is not defined")

    game_analysis[key_val] = video_event_translator(game_analysis['time_line_events'], game_analysis['video_analysis'])
    save_game_analysis(game_id, game_analysis, client)


def update_game(game_id, game, match_data, bracket_data, client):
    print("   " + game['name'])
    if not played_game(game):
        return None

    game_analysis = dict()
    collection = client.lol.game_analysis
    for item in collection.find({"_id": mongodb_id_convert(game_id)}):
        game_analysis = item

    game_analysis['league'] = bracket_data['league']
    game_analysis['tournament_id'] = bracket_data['tournament_id']
    game_analysis['bracket_id'] = bracket_data['bracket_id']
    game_analysis['match_id'] = match_data['id']
    game_analysis['game_id'] = game_id
    game_analysis['name'] = game['name']
    if "complete" != game_analysis.get('status', "incomplete"):
        url = BRACKET_DATA_URL % bracket_data + "/matches/" + match_data['id'] + "/games/" + game_id
        game_data = request_api_resource(url, retry=3, time_between=1)

        try:
            do_timeline_event_analysis(game_id, game_data, game_analysis, client)
        except Exception as e:
            save_game_analysis(game_id, game_analysis, client, error_msg={'time_line_events', e.message})

        try:
            do_timeline_infographic_analysis(game_id, game_data, game_analysis, client)
        except Exception as e:
            save_game_analysis(game_id, game_analysis, client, error_msg={'time_line_infographic', e.message})

        try:
            do_timeline_video_analysis(game_id, game_data, game_analysis, client)
        except Exception as e:
            save_game_analysis(game_id, game_analysis, client, error_msg={'video_analysis', e.message})

        try:
            do_timeline_video_translation(game_id, game_data, game_analysis, client)
        except Exception as e:
            save_game_analysis(game_id, game_analysis, client, error_msg={'event_translation', e.message})
    return game_analysis


def update_match(match_data, bracket_data, client):
    match_games = []
    for game_id, game in match_data.get('games', dict()).iteritems():
        game_analysis = update_game(game_id, game, match_data, bracket_data, client)
        if game_analysis:
            match_games.append(game_analysis)
    return match_games
