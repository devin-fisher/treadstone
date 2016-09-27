import os
import sys
from collections import OrderedDict
import time
import requests
import requests_cache
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from lib.util.static_vals import CACHE_DIR
from lib.util.mongo_util import mongodb_id_convert

requests_cache.install_cache(os.path.join(CACHE_DIR, 'lcs_schedule_cache'), expire_after=3600.0, backend='memory')

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
            return None
        else:
            time.sleep(time_between)

    raise Exception('Unable to retrieve json recourse')


def find_tournament(tournament_id, tournament_data):
    for tournament in tournament_data.get('highlanderTournaments', []):
        if tournament_id == tournament['id']:
            return tournament
    return None


def find_games(league_id, tournament_id, bracket_id, match_id):
    league_data = request_json_resource(LEAGUE_INFO_API % league_id, retry=3, time_between=1)
    tournament_data = find_tournament(tournament_id, league_data)

    if tournament_data is None:
        return None

    bracket_data = tournament_data['brackets'].get(bracket_id, None)

    if bracket_data is None:
        return None

    match_data = bracket_data['matches'].get(match_id, None)

    if match_data is None:
        return None

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
        return g_list
    else:
        return None
