import falcon
import requests
import requests_cache
import dateutil.parser
import time
import json

from collections import OrderedDict

requests_cache.install_cache('/tmp/lcs_schedule_cache', expire_after=3600.0)

LEAGUE_INFO_API = 'http://api.lolesports.com/api/v1/leagues?slug=%s'
MATCH_DETAIL_API = 'http://api.lolesports.com/api/v2/highlanderMatchDetails?tournamentId=%s&matchId=%s'
TIME_LINE_API = 'https://acs.leagueoflegends.com/v1/stats/game/%s/%s/timeline?gameHash=%s'
GAME_STAT_API = 'https://acs.leagueoflegends.com/v1/stats/game/%s/%s?gameHash=%s'


def request_json_resource(url, retry=3, time_between=1):
    for i in xrange(retry):
        response = requests.get(url, headers={'Origin':'http://www.lolesports.com'})
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
