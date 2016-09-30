#!/usr/bin/env python

from pymongo import MongoClient
import hashlib
import requests
import requests_cache
import time
from collections import OrderedDict
import sys
import os
import argparse
import json
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from lib.timeline_analysis.events import report as timeline_events
from lib.timeline_analysis.infographic import infographic_list_builder as timeline_infographic
from lib.report.report_builder import build_report_file
from lib.video.video_analysis import start_only_analysis
from lib.image_generator.image_build import build_info_graphics
from lib.timeline_analysis.video_cooralator import video_event_translator

from lib.util.static_vals import REPORTS_DIR

# BRACKET_DATA_URL = "http://127.0.0.1:8555/api/leagues/%(league)s/tournaments/%(tournament_id)s/brackets/%(bracket_id)s"
BRACKET_DATA_URL = "http://127.0.0.1/api/leagues/%(league)s/tournaments/%(tournament_id)s/brackets/%(bracket_id)s"


def mongodb_id_convert(id):
    return hashlib.md5(id).hexdigest()[:24]


def meets_schedule(bracket):
    return True


def played_game(game_data):
    if game_data.get('gameId', None):
        return True

    return False


def save_game_analysis(game_id, game_analysis, client, status='incomplete', error_msg=None):
    coll = client.lol.game_analysis
    if '_id' not in game_analysis:
        game_analysis['_id'] = mongodb_id_convert(game_id)

    if status:
        game_analysis['status'] = status
    if error_msg:
        game_analysis['error_msg'] = error_msg

    coll.save(game_analysis)


def http_get_resource(url, retry=3, time_between=1):
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


def get_game_length(stats_url):
    if stats_url is None:
        pass
        # TODO Throw an exception

    stats_data = http_get_resource(stats_url)
    length = stats_data.get('gameDuration', None)
    if length is None:
        # TODO Throw an exception
        pass
    return length


def download_video(youtube_url, game_id):
    path = '/tmp/%s.mp4' % game_id
    os.system("youtube-dl -f 22 -o '" + path + "' -q " + youtube_url)
    return path


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
    video_path = download_video(game_data.get('youtube_url', None), game_id)
    analysis = start_only_analysis(video_path, length, verbose=True)
    os.system("rm -f " + video_path)
    # print analysis
    game_analysis[key_val] = analysis
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


def update_match(match_data, bracket_data, client):
    match_games = []
    for game_id, game in match_data.get('games', dict()).iteritems():
        print("   "+game['name'])
        if not played_game(game):
            continue

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
            game_data = http_get_resource(url, retry=3, time_between=1)

            try:
                do_timeline_event_analysis(game_id, game_data, game_analysis, client)
                do_timeline_infographic_analysis(game_id, game_data, game_analysis, client)
                do_timeline_video_analysis(game_id, game_data, game_analysis, client)
                do_timeline_video_translation(game_id, game_data, game_analysis, client)
                save_game_analysis(game_id, game_analysis, client, status='complete')
                # break
            except Exception as e:
                save_game_analysis(game_id, game_analysis, client, status='error', error_msg=e.message)
        match_games.append(game_analysis)

    build_report_file(match_games, match_data['id'], os.path.join(REPORTS_DIR, match_data['id']+".zip"))


sample_bracket = {
    "_id": "57d31a4e4527ea510a02985d"
    , "league": "na-lcs"
    , "tournament_id": "472c44a9-49d3-4de4-912c-aa4151fd1b3b"
    , "bracket_id": "2a6a824d-3009-4d23-9c83-859b7a9c2629"
    }


def main(args):
    brackets = []
    client = MongoClient()
    if args.bracket is None:
        collection = client.lol.watched_brackets
        brackets = collection.find()

    for bracket in brackets:
        if args.verbose:
            print json.dumps(bracket, indent=2)

        if not bracket.get('watched', True):
            continue

        if bracket.get('complete', False):
            continue

        if not meets_schedule(bracket):
            continue

        print "Scanning Bracket '%(bracket_id)s'" % bracket
        bracket_data_url = BRACKET_DATA_URL % bracket
        if args.verbose:
            print bracket_data_url
        bracket_data = http_get_resource(bracket_data_url)
        if args.verbose:
            print json.dumps(bracket_data, indent=2)

        for match_id, match in bracket_data.get('matches', dict()).iteritems():
            print "MATCH: %(id)s - %(name)s - %(state)s" % match
            if match.get('state', '') == 'resolved':
                print(match['name'])
                update_match(match, bracket, client)
                # break

# if __name__ == "__main__":
    # img = build_info_graphics(timeline_infographic(
    # 'https://acs.leagueoflegends.com/v1/stats/game/TRLH1/1001760159/timeline?gameHash=f26accda4d6c5d59'
    # , 'https://acs.leagueoflegends.com/v1/stats/game/TRLH1/1001760159?gameHash=f26accda4d6c5d59'))
    # img[0].show()

    # events = timeline_events('https://acs.leagueoflegends.com/v1/stats/game/TRLH1/1001800106/timeline?gameHash=0e95d971fc903f68', None)
    # import lib.video.video_still_test as video_still_test
    # video_breaks = video_still_test.SAMPLE_ANALYSIS['/home/devin.fisher/Kingdoms/lol/fmqeavjSfTg.mp4']
    # print json.dumps(video_event_translator(events, video_breaks), indent=2)
    # pass

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create a highlight report for particular match.")
    parser.add_argument("-v", "--verbose", action="store_false", help="Verbosity")
    parser.add_argument("-b", "--bracket", action="store", help="Explicit Bracket Id")

    args = parser.parse_args()
    main(args)
