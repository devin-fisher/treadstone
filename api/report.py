import sys
import os
import falcon
from league import GameList

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

games_list = GameList()


class Report(object):
    def on_get(self, req, resp, league_id, tournament_id, bracket_id, match_id):
        games = None

        if not games:
            raise falcon.HTTPNotFound()

        resp.data = ""
        resp.content_type = "application/zip"
        resp.append_header('Content-Disposition', 'attachment; filename=complete_report.zip')


