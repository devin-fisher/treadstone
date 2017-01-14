#!/usr/bin/env python

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
from lib.timeline_analysis.infographic import infographic_list_builder
from lib.timeline_analysis.events import report
from lib.image_generator.image_build import build_info_graphics

if __name__ == "__main__":
    url = "https://acs.leagueoflegends.com/v1/stats/game/TRLH1/1001770101/timeline?gameHash=101e59a94cf6f805"
    stats = "https://acs.leagueoflegends.com/v1/stats/game/TRLH1/1001770101?gameHash=101e59a94cf6f805"
    info = infographic_list_builder(url, stats)
    # print (info)
    images = build_info_graphics(info)
    images[5].show()
    images[5].save('/tmp/test.png', 'PNG')


# if __name__ == "__main__":
#     url = "https://acs.leagueoflegends.com/v1/stats/game/TRLH1/1001770101/timeline?gameHash=101e59a94cf6f805"
#     stats = "https://acs.leagueoflegends.com/v1/stats/game/TRLH1/1001770101?gameHash=101e59a94cf6f805"
#     print (report(url, stats))