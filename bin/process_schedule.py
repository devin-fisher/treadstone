#!/usr/bin/env python

import requests
import requests_cache
requests_cache.install_cache('/tmp/lcs_schedule_cache', expire_after=3600.0)
import json
import dateutil.parser
import hashlib

from collections import OrderedDict

LEAGUE_INFO_API = 'http://api.lolesports.com/api/v1/leagues?slug=%s'
MATCH_DETAIL_API = 'http://api.lolesports.com/api/v2/highlanderMatchDetails?tournamentId=%s&matchId=%s'
TIME_LINE_API = 'https://acs.leagueoflegends.com/v1/stats/game/%s/%s/timeline?gameHash=%s'

def get_match_info(match_id, tournament_id):
    url = MATCH_DETAIL_API % (tournament_id, match_id)
    response = requests.get(url)
    data = response.json()

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
            scheduleItems = data['scheduleItems'][0]

            if 'scheduledTime' in scheduleItems:
                rtn['scheduledTime'] = scheduleItems['scheduledTime']

            if 'tags' in scheduleItems:
                    rtn['tags'] = scheduleItems['tags']

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
            game_info['timeline_url'] = TIME_LINE_API % (game_info.get('gameRealm'), game_info.get('gameId'), game_info.get('gameHash'))

        match_detail_info['videos'].get(game_info['id'])
        if match_detail_info['videos'].get(game_info['id']):
             game_info['youtube_video_url'] = match_detail_info['videos'].get(game_info['id'])

        rtn.append(game_info)
    # print rtn
    return sorted(rtn, key=lambda x: x.get('name'))


def process_bracket(bracket, tournament_id, bracket_id):
    rtn = []
    for match_id, match in bracket['matches'].iteritems():
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
        rtn.append(match_info)
        #break
    return sorted(rtn, key=lambda x: dateutil.parser.parse(x.get('scheduledTime')))

def process_highlander_tournaments(data, tournaments_name, bracket_name):
    rtn = OrderedDict()
    for tournament in data:
        if tournament['title'] in tournaments_name:
            tournament_id = tournament['id']
            for bracket_id, bracket in tournament['brackets'].iteritems():
                if bracket['name'] in bracket_name:
                    rtn[tournaments_name + '_' +tournament_id] = process_bracket(bracket, tournament_id, bracket['id'])
    return rtn

def process_league_tournament(league, tournaments_name, bracket_name):
    response = requests.get(LEAGUE_INFO_API % league)
    data = response.json()

    return process_highlander_tournaments(data['highlanderTournaments'], tournaments_name, bracket_name)


if __name__ == "__main__":
    rtn = process_league_tournament('na-lcs', 'na_2016_summer', 'regular_season')['na_2016_summer_472c44a9-49d3-4de4-912c-aa4151fd1b3b']
    rtn_str = json.dumps(rtn, indent=2)
    print(rtn_str)
    from pymongo import MongoClient
    client = MongoClient()
    collection = client.lol.scheduled_games
    for match in rtn:
        collection.save(match)
    
