#!/usr/bin/env python

from pymongo import MongoClient

import sys
import os
import argparse
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from lib.game_analysis.analysis import update_match
from lib.report.report_builder import build_report_file

BRACKET_DATA_URL = "api/leagues/%(league)s/tournaments/%(tournament_id)s/brackets/%(bracket_id)s"


def main(args_values):
    client = MongoClient()
    bracket = {
                "league": args_values.league,
                "tournament_id": args_values.tournament_id,
                "bracket_id": args_values.bracket_id
               }

    match_id = args_values.match_id
    match_data, games_data = update_match(match_id, bracket, client)
    zip_file_name = os.path.join("/tmp/", match_data.get("name", None) + "_" + match_id + ".zip")
    build_report_file(games_data, match_data, match_name=match_data.get("name", None), file_path=zip_file_name)
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
