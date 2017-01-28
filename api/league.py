import os
import sys
import falcon
import requests
import requests_cache
import time
import json
from collections import OrderedDict
from bson.objectid import ObjectId
from pymongo import MongoClient

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from lib.util.static_vals import CACHE_DIR
from lib.util.static_vals import REPORTS_DIR
from lib.util.mongo_util import mongodb_id_convert
from lib.report.report_builder import build_report_file_name

requests_cache.install_cache(os.path.join(CACHE_DIR, 'lcs_schedule_cache'), expire_after=240.0)

LEAGUE_INFO_API = 'http://api.lolesports.com/api/v1/leagues?slug=%s'
LEAGUE_INFO_API2 = 'http://api.lolesports.com/api/v1/scheduleItems?leagueId=%s'
MATCH_DETAIL_API = 'http://api.lolesports.com/api/v2/highlanderMatchDetails?tournamentId=%s&matchId=%s'
TIME_LINE_API = 'https://acs.leagueoflegends.com/v1/stats/game/%s/%s/timeline?gameHash=%s'
GAME_STAT_API = 'https://acs.leagueoflegends.com/v1/stats/game/%s/%s?gameHash=%s'

SLUG_ID_MAP = {"na-lcs": 2, "worlds": 9, "eu-lcs": 3}
LEAGUE_LIST = [
    {"id": "na-lcs", "name": "LCS NA", "numeric_id": 2}
    , {"id": "worlds", "name": "Worlds", "numeric_id": 9}
    , {"id": "eu-lcs", "name": "LCS EU", "numeric_id": 3}
]


def request_json_resource(url, retry=3, time_between=1):
    for i in xrange(retry):
        response = requests.get(url, headers={'Origin': 'http://www.lolesports.com'})
        if response.status_code == 200:
            return response.json(object_pairs_hook=OrderedDict)
        elif response.status_code == 404:
            raise falcon.HTTPNotFound()
        else:
            time.sleep(time_between)

    raise Exception('Unable to retrieve json recourse')


def _get_league_data(league_id):
    return request_json_resource(LEAGUE_INFO_API2 % (SLUG_ID_MAP.get(league_id, '')))


def _get_league_info(league_id):
    return request_json_resource(LEAGUE_INFO_API % league_id)


def find_tournament(tournament_id, tournament_data):
    for tournament in tournament_data.get('highlanderTournaments', []):
        if tournament_id == tournament['id']:
            return tournament
    return None


def _find_scheduled_time(match_id, league_data):
    schedule_items = league_data.get('scheduleItems', [])
    for item in schedule_items:
        if item.get('match', "") == match_id:
            return item.get('scheduledTime', "")
    return ""


def augment_game_data(game_data, match_details):
    game_hash = None
    game_id = game_data['id']
    for mapping in match_details['gameIdMappings']:
        if game_id == mapping.get('id', None):
            game_hash = mapping.get('gameHash', None)
            break

    if game_data.get('gameRealm', None) and game_data.get('gameId', None) and game_hash:
        game_data['timeline_url'] = TIME_LINE_API % (game_data.get('gameRealm'), game_data.get('gameId'), game_hash)
        game_data['stats_url'] = GAME_STAT_API % (game_data.get('gameRealm'), game_data.get('gameId'), game_hash)

    youtube_url = None
    for video in match_details['videos']:
        if game_id == video.get('game', None):
            youtube_url = video.get('source', None)
            break

    if youtube_url:
        game_data['youtube_url'] = youtube_url

    return game_data


class League(object):
    def on_get(self, req, resp, league_id):
        league_data = _get_league_info(league_id)
        resp.content_type = 'application/json'
        resp.status = falcon.HTTP_200
        resp.body = json.dumps(league_data.get('leagues'))


class LeagueList(object):
    def on_get(self, req, resp):
        resp.content_type = 'application/json'
        resp.status = falcon.HTTP_200
        resp.body = json.dumps(LEAGUE_LIST)


class Tournament(object):
    def on_get(self, req, resp, league_id, tournament_id):
        league_data = _get_league_data(league_id)
        tournament_data = find_tournament(tournament_id, league_data)

        if tournament_data:
            resp.content_type = 'application/json'
            resp.status = falcon.HTTP_200
            resp.body = json.dumps(tournament_data)
        else:
            raise falcon.HTTPNotFound()


class TournamentList(object):
    def on_get(self, req, resp, league_id):
        league_data = _get_league_data(league_id)

        tournament_list = []
        for tournament in league_data.get('highlanderTournaments', []):
            t = dict()
            t['league_id'] = league_id
            t['id'] = tournament['id']
            t['name'] = tournament['title']
            tournament_list.append(t)

        if tournament_list:
            resp.content_type = 'application/json'
            resp.status = falcon.HTTP_200
            resp.body = json.dumps(tournament_list)
        else:
            raise falcon.HTTPNotFound()


class Bracket(object):
    def on_get(self, req, resp, league_id, tournament_id, bracket_id):
        league_data = _get_league_data(league_id)
        tournament_data = find_tournament(tournament_id, league_data)
        if tournament_data is None:
            raise falcon.HTTPNotFound()

        bracket_data = tournament_data['brackets'].get(bracket_id, None)

        if bracket_data:
            resp.content_type = 'application/json'
            resp.status = falcon.HTTP_200
            resp.body = json.dumps(bracket_data)
        else:
            raise falcon.HTTPNotFound()


class BracketList(object):
    def on_get(self, req, resp, league_id, tournament_id):
        league_data = _get_league_data(league_id)
        tournament_data = find_tournament(tournament_id, league_data)
        if tournament_data is None:
            raise falcon.HTTPNotFound()

        client = MongoClient()
        brackets_coll = client.lol.watched_brackets
        b_list = []
        for bracket_id, bracket in tournament_data.get('brackets', {}).iteritems():
            watched = False
            watched_bracket = brackets_coll.find_one({'_id': mongodb_id_convert(bracket_id)})
            if watched_bracket:
                watched = watched_bracket.get('watched', watched)
            b = OrderedDict()
            b['league_id'] = league_id
            b['tournament_id'] = tournament_id
            b['id'] = bracket_id
            b['name'] = bracket['name']
            b['watched'] = watched
            b_list.append(b)

        if b_list:
            resp.content_type = 'application/json'
            resp.status = falcon.HTTP_200
            resp.body = json.dumps(b_list)
        else:
            raise falcon.HTTPNotFound()


class Match(object):
    def on_get(self, req, resp, league_id, tournament_id, bracket_id, match_id):
        league_data = _get_league_data(league_id)
        tournament_data = find_tournament(tournament_id, league_data)
        if tournament_data is None:
            raise falcon.HTTPNotFound()

        bracket_data = tournament_data['brackets'].get(bracket_id, None)

        if bracket_data is None:
            raise falcon.HTTPNotFound()

        match_data = bracket_data['matches'].get(match_id, None)

        if match_data:
            match_data['league_id'] = league_id
            match_data['tournament_id'] = tournament_id
            match_data['tournament_title'] = tournament_data['title']
            match_data['tournament_description'] = tournament_data['description']
            match_data['bracket_id'] = bracket_id
            match_data['scheduledTime'] = _find_scheduled_time(match_id, league_data)
            resp.content_type = 'application/json'
            resp.status = falcon.HTTP_200
            resp.body = json.dumps(match_data)
        else:
            raise falcon.HTTPNotFound()


class MatchList(object):
    def on_get(self, req, resp, league_id, tournament_id, bracket_id):
        league_data = _get_league_data(league_id)
        tournament_data = find_tournament(tournament_id, league_data)
        if tournament_data is None:
            raise falcon.HTTPNotFound()

        bracket_data = tournament_data['brackets'].get(bracket_id, None)

        if bracket_data is None:
            raise falcon.HTTPNotFound()

        m_list = []
        for match_id, match in bracket_data.get('matches', {}).iteritems():
            m = OrderedDict()
            m['league_id'] = league_id
            m['tournament_id'] = tournament_id
            m['bracket_id'] = bracket_id
            m['id'] = match_id
            m['name'] = match['name']
            m['state'] = match['state']
            m['position'] = match['position']
            m['has_report'] = False
            m['scheduledTime'] = _find_scheduled_time(match_id, league_data)
            report_file_loc = build_report_file_name(match['name'], match_id)
            if os.path.isfile(report_file_loc):
                m['has_report'] = True

            client = MongoClient()
            if client.lol.game_analysis.count({'match_id': match_id, 'error_msg': { '$exists': True}}) > 0:
                m['has_error'] = True

            m_list.append(m)

        m_list = sorted(m_list, key=lambda k: k.get('scheduledTime', ''))

        if m_list:
            resp.content_type = 'application/json'
            resp.status = falcon.HTTP_200
            resp.body = json.dumps(m_list)
        else:
            raise falcon.HTTPNotFound()


class Game(object):
    def on_get(self, req, resp, league_id, tournament_id, bracket_id, match_id, game_id):
        league_data = _get_league_data(league_id)
        tournament_data = find_tournament(tournament_id, league_data)

        if tournament_data is None:
            raise falcon.HTTPNotFound()

        bracket_data = tournament_data['brackets'].get(bracket_id, None)

        if bracket_data is None:
            raise falcon.HTTPNotFound()

        match_data = bracket_data['matches'].get(match_id, None)

        if match_data is None:
            raise falcon.HTTPNotFound()

        game_data = match_data['games'].get(game_id, None)

        if game_data is None:
            raise falcon.HTTPNotFound()

        match_detail_data = request_json_resource(MATCH_DETAIL_API % (tournament_id, match_id), retry=3, time_between=1)

        augmented_game_data = augment_game_data(game_data, match_detail_data)

        if augmented_game_data:
            resp.content_type = 'application/json'
            resp.status = falcon.HTTP_200
            resp.body = json.dumps(augmented_game_data)
        else:
            raise falcon.HTTPNotFound()


class GameList(object):
    def on_get(self, req, resp, league_id, tournament_id, bracket_id, match_id):
        league_data = _get_league_data(league_id)
        tournament_data = find_tournament(tournament_id, league_data)

        if tournament_data is None:
            raise falcon.HTTPNotFound()

        bracket_data = tournament_data['brackets'].get(bracket_id, None)

        if bracket_data is None:
            raise falcon.HTTPNotFound()

        match_data = bracket_data['matches'].get(match_id, None)

        if match_data is None:
            raise falcon.HTTPNotFound()

        g_list = []
        for game_id, game in match_data.get('games', {}).iteritems():
            g = OrderedDict()
            g['league_id'] = league_id
            g['tournament_id'] = tournament_id
            g['bracket_id'] = bracket_id
            g['match_id'] = match_id
            g['id'] = game_id
            g['name'] = game['name']
            g_list.append(g)

        if g_list:
            resp.content_type = 'application/json'
            resp.status = falcon.HTTP_200
            resp.body = json.dumps(g_list)
        else:
            raise falcon.HTTPNotFound()


class TeamInfo(object):
    def on_get(self, req, resp, league_id, tournament_id, bracket_id, match_id):
        match_detail_data = request_json_resource(MATCH_DETAIL_API % (tournament_id, match_id), retry=3, time_between=1)

        if match_detail_data:
            rtn = {}
            rtn['teams'] = match_detail_data.get('teams', {})
            rtn['players'] = match_detail_data.get('players', {})
            resp.content_type = 'application/json'
            resp.status = falcon.HTTP_200
            resp.body = json.dumps(rtn)
        else:
            raise falcon.HTTPNotFound()


class ScheduleItems(object):
    def on_get(self, req, resp, league_id, tournament_id, bracket_id, match_id):
        match_detail_data = request_json_resource(MATCH_DETAIL_API % (tournament_id, match_id), retry=3, time_between=1)

        if match_detail_data:
            rtn = {}
            rtn['scheduleItems'] = match_detail_data.get('scheduleItems', {})
            resp.content_type = 'application/json'
            resp.status = falcon.HTTP_200
            resp.body = json.dumps(rtn)
        else:
            raise falcon.HTTPNotFound()
