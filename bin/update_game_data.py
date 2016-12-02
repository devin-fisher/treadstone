#!/usr/bin/env python

from pymongo import MongoClient

import sys
import os
import argparse
import json
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from lib.game_analysis.analysis import update_match
from lib.util.http_lol_static import request_api_resource
from lib.report.report_builder import build_report_file
from lib.util.static_vals import REPORTS_DIR

BRACKET_DATA_URL = "api/leagues/%(league)s/tournaments/%(tournament_id)s/brackets/%(bracket_id)s"


def meets_schedule(bracket):
    return True


sample_bracket = {
  "league": "worlds",
  "_id": "1f32fc038b8e20fd073dbe3f",
  "tournament_id": "3c5fa267-237e-4b16-8e86-20378a47bf1c",
  "bracket_id": "4e593494-40f1-42de-8ffd-982c93cfe083",
  "watched": True
}

# {
# "_id": "57d31a4e4527ea510a02985d"
# , "league": "na-lcs"
# , "tournament_id": "472c44a9-49d3-4de4-912c-aa4151fd1b3b"
# , "bracket_id": "2a6a824d-3009-4d23-9c83-859b7a9c2629"
# , 'watched' : True
# }


def main(args):
    brackets = []
    client = MongoClient()
    if args.bracket is None:
        collection = client.lol.watched_brackets
        brackets = collection.find()

    for bracket in brackets:
        if args.verbose:
            print json.dumps(bracket, indent=2)

        if not bracket.get('watched', True):
            continue

        if bracket.get('complete', False):
            continue

        if not meets_schedule(bracket):
            continue

        print "Scanning Bracket '%(bracket_id)s'" % bracket
        bracket_data_url = BRACKET_DATA_URL % bracket
        if args.verbose:
            print bracket_data_url
        bracket_data = request_api_resource(bracket_data_url)
        if args.verbose:
            print json.dumps(bracket_data, indent=2)

        for match_id, match in bracket_data.get('matches', dict()).iteritems():
            print "MATCH: %(id)s - %(name)s - %(state)s" % match
            if match.get('state', '') == 'resolved':
                print(match['name'])
                games_data = update_match(match, bracket, client)
                build_report_file(games_data, match, match_name=match.get("name", None))
                # break

# if __name__ == "__main__":
    # img = build_info_graphics(timeline_infographic(
    # 'https://acs.leagueoflegends.com/v1/stats/game/TRLH1/1001760159/timeline?gameHash=f26accda4d6c5d59'
    # , 'https://acs.leagueoflegends.com/v1/stats/game/TRLH1/1001760159?gameHash=f26accda4d6c5d59'))
    # img[0].show()

    # events = timeline_events('https://acs.leagueoflegends.com/v1/stats/game/TRLH1/1001800106/timeline?\gameHash=0e95d971fc903f68', None)
    # import lib.video.video_still_test as video_still_test
    # video_breaks = video_still_test.SAMPLE_ANALYSIS['/home/devin.fisher/Kingdoms/lol/fmqeavjSfTg.mp4']
    # print json.dumps(video_event_translator(events, video_breaks), indent=2)
    # pass

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create a highlight report for particular match.")
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbosity")
    parser.add_argument("-b", "--bracket", action="store", help="Explicit Bracket Id")

    args = parser.parse_args()
    main(args)
