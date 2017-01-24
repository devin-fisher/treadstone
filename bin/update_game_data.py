#!/usr/bin/env python

from pymongo import MongoClient

import sys
import os
import argparse
import json
from pid import PidFile, PidFileError
import tempfile
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from lib.game_analysis.analysis import update_match
from lib.util.http_lol_static import request_api_resource
from lib.report.report_builder import build_report_file

BRACKET_DATA_URL = "api/leagues/%(league)s/tournaments/%(tournament_id)s/brackets/%(bracket_id)s/matches"

SKIPPED_MATCHES = []


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

        print "Scanning Bracket '%(bracket_id)s'" % bracket
        bracket_data_url = BRACKET_DATA_URL % bracket
        if args.verbose:
            print bracket_data_url
        matches = request_api_resource(bracket_data_url)
        if args.verbose:
            print json.dumps(matches, indent=2)

        for match in matches:
            match_id = match['id']
            if match_id not in SKIPPED_MATCHES:
                match_data, games_data = update_match(match_id, match, bracket, client)
                build_report_file(games_data, match_data, match_name=match_data.get("name", None))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create a highlight report for particular match.")
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbosity")
    parser.add_argument("-b", "--bracket", action="store", help="Explicit Bracket Id")

    args = parser.parse_args()
    try:
        with PidFile(piddir=tempfile.gettempdir()) as pid:
            main(args)
    except PidFileError as e:
        print("already running")

