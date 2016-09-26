import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

import falcon
from inmemory_zip import InMemoryZip
import json

from lib.image_generator.image_build import build_info_graphics
from lib.timeline_analysis.events import report
from lib.timeline_analysis.infographic import infographic_list_builder as timeline_infographic


HARD_CODED_INFOGRAPHIC = timeline_infographic(
            'https://acs.leagueoflegends.com/v1/stats/game/TRLH1/1001760159/timeline?gameHash=f26accda4d6c5d59',
            'https://acs.leagueoflegends.com/v1/stats/game/TRLH1/1001760159?gameHash=f26accda4d6c5d59')

HARD_CODED_EVENTS = report(
            'https://acs.leagueoflegends.com/v1/stats/game/TRLH1/1001760159/timeline?gameHash=f26accda4d6c5d59',
            'https://acs.leagueoflegends.com/v1/stats/game/TRLH1/1001760159?gameHash=f26accda4d6c5d59')


class Report(object):
    def on_get(self, req, resp, league_id, tournament_id, bracket_id):
        time_line_events = HARD_CODED_EVENTS
        time_line_infographic = HARD_CODED_INFOGRAPHIC
        images = build_info_graphics(time_line_infographic)
        imz = InMemoryZip()
        imz.append("time_line_events.json", json.dumps(time_line_events, indent=2))
        imz.append("time_line_infographic.json", json.dumps(time_line_infographic, indent=2))
        for i in range(len(images)):
            imz.append_image("infographic"+str(i), images[i])
        resp.data = imz.read()
        resp.content_type = "application/zip"
        resp.append_header('Content-Disposition', 'attachment; filename=complete_report.zip')


