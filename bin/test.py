#!/usr/bin/env python

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
from lib.timeline_analysis.infographic import infographic_list_builder
from lib.timeline_analysis.events import report

if __name__ == "__main__":
    url = "https://acs.leagueoflegends.com/v1/stats/game/TRLH1/1001770101/timeline?gameHash=101e59a94cf6f805"
    stats = "https://acs.leagueoflegends.com/v1/stats/game/TRLH1/1001770101?gameHash=101e59a94cf6f805"
    print (infographic_list_builder(url, stats))

if __name__ == "__main__":
    url = "https://acs.leagueoflegends.com/v1/stats/game/TRLH1/1001770101/timeline?gameHash=101e59a94cf6f805"
    stats = "https://acs.leagueoflegends.com/v1/stats/game/TRLH1/1001770101?gameHash=101e59a94cf6f805"
    print (report(url, stats))