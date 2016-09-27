import sys
import os
import falcon
from inmemory_zip import InMemoryZip
import json
from pymongo import MongoClient
from league import GameList
from league_functions import find_games

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from lib.image_generator.image_build import build_info_graphics
# from lib.timeline_analysis.events import report
# from lib.timeline_analysis.infographic import infographic_list_builder as timeline_infographic
from lib.util.mongo_util import mongodb_id_convert

games_list = GameList()
#
#
# HARD_CODED_INFOGRAPHIC = timeline_infographic(
#             'https://acs.leagueoflegends.com/v1/stats/game/TRLH1/1001760159/timeline?gameHash=f26accda4d6c5d59',
#             'https://acs.leagueoflegends.com/v1/stats/game/TRLH1/1001760159?gameHash=f26accda4d6c5d59')
#
# HARD_CODED_EVENTS = report(
#             'https://acs.leagueoflegends.com/v1/stats/game/TRLH1/1001760159/timeline?gameHash=f26accda4d6c5d59',
#             'https://acs.leagueoflegends.com/v1/stats/game/TRLH1/1001760159?gameHash=f26accda4d6c5d59')

class Report(object):
    def on_get(self, req, resp, league_id, tournament_id, bracket_id, match_id):
        games = find_games(league_id, tournament_id, bracket_id, match_id)

        client = MongoClient()

        if not games:
            raise falcon.HTTPNotFound()

        imz = InMemoryZip()
        had_data = False
        for game in games:
            name = game['name']
            game_coll = client.lol.game_analysis
            game_analysis = game_coll.find_one({'_id': mongodb_id_convert(game['id'])})
            if not game_analysis or 'time_line_events' not in game_analysis or 'time_line_infographic' not in game_analysis:
                continue

            had_data = True
            time_line_events = game_analysis['time_line_events']
            time_line_infographic = game_analysis['time_line_infographic']
            images = build_info_graphics(time_line_infographic)

            imz.append(name+"_time_line_events.json", json.dumps(time_line_events, indent=2))
            imz.append(name+"_time_line_infographic.json", json.dumps(time_line_infographic, indent=2))
            for i in range(len(images)):
                imz.append_image(name+"_infographic"+str(i), images[i])

        if not had_data:
            raise falcon.HTTPNotFound()
        resp.data = imz.read()
        resp.content_type = "application/zip"
        resp.append_header('Content-Disposition', 'attachment; filename=complete_report.zip')


