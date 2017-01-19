import sys
import os
import falcon
from league import GameList
import glob

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
from lib.util.static_vals import REPORTS_DIR
games_list = GameList()


class Report(object):
    def on_get(self, req, resp, league_id, tournament_id, bracket_id, match_id):
        file_list = glob.glob(os.path.join(REPORTS_DIR, "*" + match_id + ".zip"))
        if file_list:
            path = file_list[0]

        if not os.path.isfile(path):
            raise falcon.HTTPNotFound()

        resp.stream = open(path, 'rb')
        resp.stream_len = os.path.getsize(path)
        resp.content_type = "application/zip"
        resp.append_header('Content-Disposition', 'attachment; filename=complete_report.zip')


