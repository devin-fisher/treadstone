#!/usr/bin/env python

import os
import sys
from pymongo import MongoClient
# from bson.objectid import ObjectId
import hashlib
import requests
import time
from collections import OrderedDict

from lib.timeline_analysis.events import report as timeline_events
from lib.timeline_analysis.infographic import infographic_list_builder as timeline_infographic
from lib.video.video_analysis import standard_analysis

import json


BRACKET_DATA_URL = "http://127.0.0.1:8000/api/league/%(league)s/tournaments/%(tournament_id)s/brackets/%(bracket_id)s"


def mongodb_id_convert(id):
    return hashlib.md5(id).hexdigest()[:24]


def meets_schedule(bracket):
    return True


def played_game(game_data):
    if game_data.get('gameId', None):
        return True

    return False


def save_game_analysis(game_id, game_analysis, client):
    coll = client.lol.game_analysis
    if '_id' not in game_analysis:
        game_analysis['_id'] = mongodb_id_convert(game_id)
    coll.save(game_analysis)


def http_get_resource(url, retry=3, time_between=1):
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
    os.system("youtube-dl -o '" + path + "' -q " + youtube_url)
    return path


def _timeline_analysis(func, key_val, game_id, game_data, game_analysis, client):
    if key_val in game_analysis:
        return game_analysis

    url = game_data.get('timeline_url', None)
    if url is None:
        raise Exception("Time Line URL is not defined")

    game_analysis[key_val] = func(url)
    save_game_analysis(game_id, game_analysis, client)

    return game_analysis


def do_timeline_event_analysis(game_id, game_data, game_analysis, client):
    _timeline_analysis(timeline_events, 'time_line_events', game_id, game_data, game_analysis, client)


def do_timeline_infographic_analysis(game_id, game_data, game_analysis, client):
    _timeline_analysis(timeline_infographic, 'time_line_infographic', game_id, game_data, game_analysis, client)


def do_game_analysis(game_id, game_data, game_analysis, client):
    length = get_game_length(game_data.get('stats_url', None))
    video_path = download_video(game_data.get('youtube_url', None), game_id)
    print(standard_analysis(video_path, length, verbose=True))
    return game_analysis


def update_match(match_data, bracket_data, client):
    for game_id, game in match_data.get('games', dict()).iteritems():
        if not played_game(game):
            continue

        collection = client.lol.game_analysis
        game_analysis = dict()
        for item in collection.find({"_id": mongodb_id_convert(game_id)}):
            game_analysis = item

        if not game_analysis.get('complete', False):
            url = BRACKET_DATA_URL % bracket_data + "/matches/" + match_data['id'] + "/games/" + game_id
            game_data = http_get_resource(url, retry=3, time_between=1)
            print str(game_data)

            do_timeline_event_analysis(game_id, game_data, game_analysis, client)
            do_timeline_infographic_analysis(game_id, game_data, game_analysis, client)
            # do_game_analysis(game_id, game_data, game_analysis, client)
            # break


def main(args):
    client = MongoClient()
    collection = client.lol.watched_brackets
    for bracket in collection.find():
        if not bracket.get('watched', True):
            continue

        if bracket.get('complete', False):
            continue

        if not meets_schedule(bracket):
            continue

        bracket_data = http_get_resource(BRACKET_DATA_URL % bracket)

        for match_id, match in bracket_data.get('matches', dict()).iteritems():
            if match.get('state', '') == 'resolved':
                update_match(match, bracket, client)
                # break


if __name__ == "__main__":
    main(None)