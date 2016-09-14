#!/usr/bin/env python

import requests
import requests_cache
import dateutil.parser
import hashlib
import time
import json
# from pymongo import MongoClient

from collections import OrderedDict

requests_cache.install_cache('/tmp/lcs_schedule_cache', expire_after=3600.0)

LEAGUE_INFO_API = 'http://api.lolesports.com/api/v1/leagues?slug=%s'
MATCH_DETAIL_API = 'http://api.lolesports.com/api/v2/highlanderMatchDetails?tournamentId=%s&matchId=%s'
                 # 'http://api.lolesports.com/api/v2/highlanderMatchDetails?tournamentId=%s&matchId=%s'
TIME_LINE_API = 'https://acs.leagueoflegends.com/v1/stats/game/%s/%s/timeline?gameHash=%s'


def request_json_resource(url, retry=3, time_between=1):
    for i in xrange(retry):
        response = requests.get(url, headers={'Origin':'http://www.lolesports.com'})
        if response.status_code == 200:
            return response.json()
        else:
            time.sleep(time_between)

    raise Exception('Unable to retrieve json recourse')


def get_match_info(match_id, tournament_id):
    url = MATCH_DETAIL_API % (tournament_id, match_id)
    print(url)
    data = request_json_resource(url)

    rtn = OrderedDict()

    rtn['videos'] = {}
    rtn_videos = rtn['videos']
    if 'videos' in data:
        for video in data['videos']:
            rtn_videos[video['game']] = video['source']

    rtn['mapping'] = {}
    rtn_hashes = rtn['mapping']
    if 'gameIdMappings' in data:
        for mapping in data['gameIdMappings']:
            rtn_hashes[mapping['id']] = mapping['gameHash']

    if 'scheduleItems' in data:
        if len(data['scheduleItems']) > 0:
            schedule_items = data['scheduleItems'][0]

            if 'scheduledTime' in schedule_items:
                rtn['scheduledTime'] = schedule_items['scheduledTime']

            if 'tags' in schedule_items:
                rtn['tags'] = schedule_items['tags']

    # print data
    return rtn


def get_game_info(games, match_detail_info):
    rtn = []
    for id, game in games.iteritems():
        game_info = OrderedDict()
        game_info['name'] = game['name']
        game_info['id'] = game['id']
        game_info['gameId'] = game.get('gameId')
        game_info['gameRealm'] = game.get('gameRealm')
        game_info['gameHash'] = match_detail_info['mapping'].get(game_info['id'])

        if game_info.get('gameRealm') and game_info.get('gameId') and game_info.get('gameHash'):
            game_info['timeline_url'] = TIME_LINE_API % (
                game_info.get('gameRealm'), game_info.get('gameId'), game_info.get('gameHash'))

        match_detail_info['videos'].get(game_info['id'])
        if match_detail_info['videos'].get(game_info['id']):
            game_info['youtube_video_url'] = match_detail_info['videos'].get(game_info['id'])

        rtn.append(game_info)
    # print rtn
    return sorted(rtn, key=lambda x: x.get('name'))


def get_match_info(tournament_id, bracket_id, match_id, match):
    match_detail_info = get_match_info(match_id, tournament_id)
    match_info = OrderedDict()
    match_info['name'] = match['name']
    match_info['id'] = match_id
    match_info['_id'] = hashlib.md5(match_id).hexdigest()[:24]
    match_info['scheduledTime'] = match_detail_info.get('scheduledTime')
    match_info['tournament_id'] = tournament_id
    match_info['bracket_id'] = bracket_id
    match_info['state'] = match['state']
    match_info['games'] = get_game_info(match['games'], match_detail_info)
    match_info['tags'] = match_detail_info.get('tags')


def process_bracket(bracket, tournament_id, bracket_id):
    matches = []
    for match_id, match in bracket['matches'].iteritems():
        matches.append(get_match_info(tournament_id, bracket_id, match_id, match))
        # break
    return sorted(matches, key=lambda x: dateutil.parser.parse(x.get('scheduledTime')))


def process_highlander_tournaments(data, tournaments_name, bracket_name):
    matches = [] 
    brackets = []
    for tournament in data:
        if tournament['title'] in tournaments_name:
            tournament_id = tournament['id']
            for bracket_id, bracket in tournament['brackets'].iteritems():
                if bracket['name'] in bracket_name:
                    matches.extend(process_bracket(bracket, tournament_id, bracket['id']))
                    add_bracket = OrderedDict()
                    add_bracket['tournaments_name'] = tournaments_name
                    add_bracket['bracket_name'] = bracket['name']
                    add_bracket['bracket_id'] = bracket['id']
                    add_bracket['_id'] = hashlib.md5(bracket['id']).hexdigest()[:24]
                    add_bracket['tournament_id'] = tournament_id
                    brackets.append(add_bracket)
    return matches, brackets


def process_league_tournament(league, tournaments_name, bracket_name):
    data = request_json_resource(LEAGUE_INFO_API % league)
    return process_highlander_tournaments(data['highlanderTournaments'], tournaments_name, bracket_name)


def update_match(match, tournament_data):
    tournament_id = match['tournament_id']
    match_id = match['id']
    bracket_id = match['bracket_id']

    tournament_data = find_tournament(tournament_id, tournament_data)
    bracket_data = find_bracket(bracket_id, tournament_data)
    match_data = find_match(match_id, bracket_data)
    pass


def find_tournament(tournament_id, tournament_data):
    for tournament in tournament_data:
        if tournament_id == tournament['id']:
            return tournament
    return None


def find_bracket(bracket_id, tournament_data):
    return tournament_data['brackets'].get(bracket_id, None)


def find_match(match_id, bracket_data):
    return bracket_data['matches'].get(match_id, None)

sample_match = json.loads("""{ "name": "quarter-final-2", "tags": { "tournamentLabel": "urn:rg:lolesports:global:highlander:tournament:472c44a9-49d3-4de4-912c-aa4151fd1b3b", "stageLabel": "urn:rg:lolesports:global:highlander:tournament:472c44a9-49d3-4de4-912c-aa4151fd1b3b:bracket:515a7882-29b9-4896-8fb7-50309e43d677", "blockLabel": "Quarterfinals", "leagueLabel": "urn:rg:lolesports:global:league:league:2", "subBlockPrefix": "day", "subBlockLabel": "1" }, "scheduledTime": "2016-08-13T19:00:00.000+0000", "bracket_id": "515a7882-29b9-4896-8fb7-50309e43d677", "state": "unresolved", "games": [ { "gameHash": null, "gameId": null, "name": "G1", "gameRealm": null, "id": "384989d1-b990-41f8-8a7f-8442431ea33c" }, { "gameHash": null, "gameId": null, "name": "G2", "gameRealm": null, "id": "02060be3-656a-4bbb-aec0-b67c371a39d8" }, { "gameHash": null, "gameId": null, "name": "G3", "gameRealm": null, "id": "118997bb-fb4c-4336-b1ac-ad6fa91813cf" }, { "gameHash": null, "gameId": null, "name": "G4", "gameRealm": null, "id": "fef00ef6-8a35-48e7-b09e-4ebce6e81dd6" }, { "gameHash": null, "gameId": null, "name": "G5", "gameRealm": null, "id": "cb9df5d9-bb7f-4292-8c80-a611f924f2e5" } ], "_id": "1957c5af76144ae3984f5f12", "id": "7071885d-dd2c-4329-a016-2da752ef4ea0", "tournament_id": "472c44a9-49d3-4de4-912c-aa4151fd1b3b" }""")

if __name__ == "__main__":
    update_match(sample_match, request_json_resource(LEAGUE_INFO_API % 'na-lcs')['highlanderTournaments'])
    # rtn_matches, rtn_brackets = process_league_tournament('na-lcs', 'na_2016_summer', 'na_2016_summer_playoffs')
    # rtn_str = json.dumps(rtn_matches['na_2016_summer_472c44a9-49d3-4de4-912c-aa4151fd1b3b'], indent=2)
    # rtn_str = json.dumps(rtn_brackets, indent=2)
    # print(rtn_str)

    # client = MongoClient()
    #
    # collection = client.lol.scheduled_matches
    # for match in rtn_matches:
    #     collection.save(match)
    #
    # collection = client.lol.brackets
    # for bracket in rtn_brackets:
    #     collection.save(bracket)
