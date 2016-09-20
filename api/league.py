import falcon
import requests
import requests_cache
import time
import json

from collections import OrderedDict

requests_cache.install_cache('/tmp/lcs_schedule_cache', expire_after=3600.0, backend='memory')

LEAGUE_INFO_API = 'http://api.lolesports.com/api/v1/leagues?slug=%s'
MATCH_DETAIL_API = 'http://api.lolesports.com/api/v2/highlanderMatchDetails?tournamentId=%s&matchId=%s'
TIME_LINE_API = 'https://acs.leagueoflegends.com/v1/stats/game/%s/%s/timeline?gameHash=%s'
GAME_STAT_API = 'https://acs.leagueoflegends.com/v1/stats/game/%s/%s?gameHash=%s'


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


def find_tournament(tournament_id, tournament_data):
    for tournament in tournament_data.get('highlanderTournaments', []):
        if tournament_id == tournament['id']:
            return tournament
    return None


def list_tournament(tournament_data):
    rtn = []
    for tournament in tournament_data.get('highlanderTournaments', []):
        t = dict()
        t['id'] = tournament['id']
        t['name'] = tournament['title']
        rtn.append(t)
    return rtn


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
        league_data = request_json_resource(LEAGUE_INFO_API % league_id, retry=3, time_between=1)
        resp.content_type = 'application/json'
        resp.status = falcon.HTTP_200
        resp.body = json.dumps(league_data.get('leagues'))


class LeagueList(object):
    def on_get(self, req, resp):
        league_list = [{"key": "na-lcs", "name": "LCS NA"}]
        resp.content_type = 'application/json'
        resp.status = falcon.HTTP_200
        resp.body = json.dumps(league_list)


class Tournament(object):
    def on_get(self, req, resp, league_id, tournament_id):
        league_data = request_json_resource(LEAGUE_INFO_API % league_id, retry=3, time_between=1)
        tournament_data = find_tournament(tournament_id, league_data)

        if tournament_data:
            resp.content_type = 'application/json'
            resp.status = falcon.HTTP_200
            resp.body = json.dumps(tournament_data)
        else:
            raise falcon.HTTPNotFound()


class TournamentList(object):
    def on_get(self, req, resp, league_id):
        league_data = request_json_resource(LEAGUE_INFO_API % league_id, retry=3, time_between=1)
        tournament_list = list_tournament(league_data)

        if tournament_list:
            resp.content_type = 'application/json'
            resp.status = falcon.HTTP_200
            resp.body = json.dumps(tournament_list)
        else:
            raise falcon.HTTPNotFound()


class Bracket(object):
    def on_get(self, req, resp, league_id, tournament_id, bracket_id):
        league_data = request_json_resource(LEAGUE_INFO_API % league_id, retry=3, time_between=1)
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
        league_data = request_json_resource(LEAGUE_INFO_API % league_id, retry=3, time_between=1)
        tournament_data = find_tournament(tournament_id, league_data)
        if tournament_data is None:
            raise falcon.HTTPNotFound()

        # bracket_data = tournament_data['brackets'].get(bracket_id, None)

        b_list = []
        for bracket_id, bracket in tournament_data.get('brackets', {}).iteritems():
            b = OrderedDict()
            b['id'] = bracket_id
            b['name'] = bracket['name']
            b_list.append(b)

        if b_list:
            resp.content_type = 'application/json'
            resp.status = falcon.HTTP_200
            resp.body = json.dumps(b_list)
        else:
            raise falcon.HTTPNotFound()


class Match(object):
    def on_get(self, req, resp, league_id, tournament_id, bracket_id, match_id):
        league_data = request_json_resource(LEAGUE_INFO_API % league_id, retry=3, time_between=1)
        tournament_data = find_tournament(tournament_id, league_data)
        if tournament_data is None:
            raise falcon.HTTPNotFound()

        bracket_data = tournament_data['brackets'].get(bracket_id, None)

        if bracket_data is None:
            raise falcon.HTTPNotFound()

        match_data = bracket_data['matches'].get(match_id, None)

        if match_data:
            resp.content_type = 'application/json'
            resp.status = falcon.HTTP_200
            resp.body = json.dumps(match_data)
        else:
            raise falcon.HTTPNotFound()


class MatchList(object):
    def on_get(self, req, resp, league_id, tournament_id, bracket_id):
        league_data = request_json_resource(LEAGUE_INFO_API % league_id, retry=3, time_between=1)
        tournament_data = find_tournament(tournament_id, league_data)
        if tournament_data is None:
            raise falcon.HTTPNotFound()

        bracket_data = tournament_data['brackets'].get(bracket_id, None)

        if bracket_data is None:
            raise falcon.HTTPNotFound()

        m_list = []
        for match_id, match in bracket_data.get('matches', {}).iteritems():
            m = OrderedDict()
            m['id'] = match_id
            m['name'] = match['name']
            m['state'] = match['state']
            m['position'] = match['position']
            m_list.append(m)

        if m_list:
            resp.content_type = 'application/json'
            resp.status = falcon.HTTP_200
            resp.body = json.dumps(m_list)
        else:
            raise falcon.HTTPNotFound()


class Game(object):
    def on_get(self, req, resp, league_id, tournament_id, bracket_id, match_id, game_id):
        league_data = request_json_resource(LEAGUE_INFO_API % league_id, retry=3, time_between=1)
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
        league_data = request_json_resource(LEAGUE_INFO_API % league_id, retry=3, time_between=1)
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
            g['id'] = game_id
            g['name'] = game['name']
            g_list.append(g)

        if g_list:
            resp.content_type = 'application/json'
            resp.status = falcon.HTTP_200
            resp.body = json.dumps(g_list)
        else:
            raise falcon.HTTPNotFound()
