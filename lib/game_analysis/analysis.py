import time
from dateutil.parser import parse
import datetime

from lib.game_analysis.video_dowload import YoutubeFile
from lib.timeline_analysis.events import report as timeline_events
from lib.timeline_analysis.infographic import infographic_list_builder as timeline_infographic
from lib.video.video_analysis import standard_analysis as video_analysis
from lib.timeline_analysis.video_cooralator import video_event_translator
from lib.util.mongo_util import mongodb_id_convert
from lib.util.http_lol_static import request_api_resource, request_json_resource_cacheless
from lib.game_analysis.youtube_url import find_youtube_url


MATCH_DATA_URL = "api/leagues/%(league)s/tournaments/%(tournament_id)s/brackets/%(bracket_id)s/matches/%(match_id)s"
GAME_DATA_URL = "api/leagues/%(league_id)s/tournaments/%(tournament_id)s/brackets/%(bracket_id)s/matches/%(id)s"  # inconsitent league_id vs league


class NotReadyException(Exception):
    pass


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
        error_list.append(str(error_msg))
        game_analysis['error_msg'] = error_list

    game_analysis['time_stamp'] = int(time.time())

    coll.save(game_analysis)


def get_game_length(stats_url):
    if stats_url is None:
        raise NotReadyException("Stats URL for game was not defined")

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
        raise NotReadyException("Time Line URL is not defined")

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

    stats_url = game_data.get('stats_url', None)
    if stats_url is None:
        raise NotReadyException("Stats URL is not defined")

    length = get_game_length(stats_url)
    youtube_url = find_youtube_url(game_id, game_data, game_analysis, client)

    if youtube_url is None:
        raise NotReadyException("Unable to find youtube url")

    with YoutubeFile(youtube_url, game_id) as video_path:
        analysis = video_analysis(video_path, length, verbose=False)

    # print analysis
    game_analysis[key_val] = analysis
    game_analysis['youtube_url'] = youtube_url
    save_game_analysis(game_id, game_analysis, client)


def do_timeline_video_translation(game_id, game_data, game_analysis, client):
    key_val = 'event_translation'
    if key_val in game_analysis:
        return game_analysis

    game_analysis[key_val] = video_event_translator(game_analysis['time_line_events'], game_analysis['video_analysis'])
    save_game_analysis(game_id, game_analysis, client)


def update_game(game_id, game, match_data, client):
    print("   " + game['name'])

    game_analysis = dict()
    collection = client.lol.game_analysis
    for item in collection.find({"_id": mongodb_id_convert(game_id)}):
        game_analysis = item

    game_analysis['league'] = match_data['league_id']
    game_analysis['tournament_id'] = match_data['tournament_id']
    game_analysis['bracket_id'] = match_data['bracket_id']
    game_analysis['match_id'] = match_data['id']
    game_analysis['match_scheduled_time'] = match_data['scheduledTime']
    game_analysis['match_name'] = match_data['name']
    game_analysis['game_id'] = game_id
    game_analysis['game_name'] = game['name']
    if is_not_complete(game_analysis):
        url = GAME_DATA_URL % match_data + "/games/" + game_id
        game_data = request_api_resource(url, retry=3, time_between=1)

        if not played_game(game_data):
            return None

        try:
            do_timeline_event_analysis(game_id, game_data, game_analysis, client)
        except NotReadyException:
            return game_analysis
        except Exception as e:
            save_game_analysis(game_id, game_analysis, client, error_msg=('time_line_events', e.message))

        try:
            do_timeline_infographic_analysis(game_id, game_data, game_analysis, client)
        except NotReadyException:
            return game_analysis
        except Exception as e:
            save_game_analysis(game_id, game_analysis, client, error_msg=('time_line_infographic', e.message))

        try:
            do_timeline_video_analysis(game_id, game_data, game_analysis, client)
        except NotReadyException:
            return game_analysis
        except Exception as e:
            save_game_analysis(game_id, game_analysis, client, error_msg=('video_analysis', e.message))

        try:
            do_timeline_video_translation(game_id, game_data, game_analysis, client)
        except Exception as e:
            save_game_analysis(game_id, game_analysis, client, error_msg=('event_translation', e.message))
    return game_analysis


def is_not_complete(game_analysis):
    # return True
    return not all(k in game_analysis for k in
               (
                   'time_line_events',
                    'time_line_infographic',
                    'video_analysis',
                    'event_translation'
                ))


def update_match(match_id, bracket_ids, client):
    ids = dict(bracket_ids)
    ids['match_id'] = match_id
    match_data = request_api_resource(MATCH_DATA_URL % ids)

    scheduled_str = match_data.get('scheduledTime', "2100-01-01")
    scheduled = None
    if scheduled_str:
        scheduled = parse(scheduled_str)

    if match_data.get('state', '') == 'resolved' or (scheduled and datetime.datetime.now() > scheduled):
        print "MATCH: %(id)s - %(name)s - %(state)s" % match_data
        print(match_data['name'])
        match_games = []
        for game_id, game in match_data.get('games', dict()).iteritems():
            game_analysis = update_game(game_id, game, match_data, client)
            if game_analysis:
                match_games.append(game_analysis)

        if match_data.get('state', '') == 'resolved':
            return match_data, match_games
        else:
            return match_data, []

    return match_data, []

if __name__ == "__main__":
    scheduled = parse({}.get('scheduledTime', "2100-01-01"))
    print (datetime.datetime.now() > scheduled)