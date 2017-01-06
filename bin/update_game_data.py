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

BRACKET_DATA_URL = "api/leagues/%(league)s/tournaments/%(tournament_id)s/brackets/%(bracket_id)s"


def meets_schedule(bracket):
    return True


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

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create a highlight report for particular match.")
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbosity")
    parser.add_argument("-b", "--bracket", action="store", help="Explicit Bracket Id")

    args = parser.parse_args()
    main(args)
