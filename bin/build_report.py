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
    client = MongoClient()
    bracket = {"league": args.league, "tournament_id": args.tournament_id, "bracket_id": args.bracket_id}
    bracket_data_url = BRACKET_DATA_URL % bracket
    if args.verbose:
        print bracket_data_url
    bracket_data = request_api_resource(bracket_data_url)
    # if args.verbose:
    #     print json.dumps(bracket_data, indent=2)

    match_id = args.match_id
    match = bracket_data.get('matches', dict()).get(match_id, None)
    if match:
        print "MATCH: %(id)s - %(name)s - %(state)s" % match
        if match.get('state', '') == 'resolved':
            print(match['name'])
            games_data = update_match(match, bracket, client)

            zip_file_name = os.path.join("/tmp/", match.get("name", None) + "_" + match_id+".zip")
            build_report_file(games_data, match, file_path=zip_file_name)
            print "created zip at " + zip_file_name

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create a highlight report for particular match.")
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbosity")

    parser.add_argument('league', metavar='LEAGUE', help='League in which the match was played')
    parser.add_argument('tournament_id', metavar='TOURNAMENT_ID', help='Tournament ID in which the match was played')
    parser.add_argument('bracket_id', metavar='BRACKET_ID', help='Bracket ID in which the match was played')
    parser.add_argument('match_id', metavar='MATCH_ID', help='Match ID of the match')

    args = parser.parse_args()
    if args.verbose:
        print("Arguments:")
        print(str(args))
    main(args)
