#!/usr/bin/env python

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
from lib.timeline_analysis.infographic import infographic_list_builder
from lib.timeline_analysis.events import report

if __name__ == "__main__":
    url = "https://acs.leagueoflegends.com/v1/stats/game/TRLH1/1001770122/timeline?gameHash=b49ec7b6e70e0ac3"
    stats = "https://acs.leagueoflegends.com/v1/stats/game/TRLH1/1001710249?gameHash=856ed19d3d6dce2e"
    print (infographic_list_builder(url, stats))

if __name__ == "__main__":
    url = "https://acs.leagueoflegends.com/v1/stats/game/TRLH1/1001770122/timeline?gameHash=b49ec7b6e70e0ac3"
    stats = "https://acs.leagueoflegends.com/v1/stats/game/TRLH1/1001710249?gameHash=856ed19d3d6dce2e"
    print (report(url, stats))