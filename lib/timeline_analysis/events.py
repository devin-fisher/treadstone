#!/usr/bin/env python
import json
import argparse
# from lib.util.http_lol_static import request_json_resource
import requests
from collections import OrderedDict

from timeline_lib import kill_list_function
from timeline_lib import start_counter_list_function
from timeline_lib import end_list_function
from timeline_lib import large_fight_function





def report(url, stats_url):
    data = request_json_resource(url)
    # r = requests.get(url)
    # data = r.json()
    counter_list = []
    kill_list = kill_list_function(data)
    start_list, counter_list = start_counter_list_function(kill_list, counter_list)
    end_list, counter_list = end_list_function(kill_list, counter_list, start_list)
    team_fight = large_fight_function(start_list, counter_list)

    before = 7000
    after = 2000
    len_start_list = len(start_list)
    video_length = 0
    # infographic_list = infographic_time_list_builder(data, team_fight)
    video_edit_times = []
    for a in range(0, len_start_list):
        video_edit_times.append({})
        seconds = int((end_list[a] / 1000) % 60)
        end_time = start_list[a] + after
        if (seconds < before):
            start_time = start_list[a] - before
        else:
            start_time = start_list[a] - before
        if (seconds > 60 - after):
            end_time = end_list[a] + after
        else:
            end_time = end_list[a] + after

        video_edit_times[a]['startTime'] = start_time
        video_edit_times[a]['endTime'] = end_time
        video_length = video_length + ((end_time - start_time)/1000)

    print(video_edit_times)
    return video_edit_times



# def infographic_time_list_builder(data,team_fight):
#     infographic_time_list = []
#     len_game = len(data['frames']) // 5
#     len_team_fight = len(team_fight)
#     time_counter = 0
#     for a in range(0,len_game):
#         time_counter = time_counter + 5
#         infographic_time = (time_counter * 60) * 1000
#         infographic_time_list.append(infographic_time)
#         for b in range(0,len_team_fight):
#             team_fight_time = int((team_fight[b]/60)/1000)
#
#             if team_fight_time > time_counter and team_fight_time < (time_counter + 5):
#                 infographic_time_list.append(team_fight[b])
#
#     return infographic_time_list


def _create_url(args):
    return "https://acs.leagueoflegends.com/v1/stats/game/TRLH1/1001720111/timeline?gameHash=55109b5a7a91ae87"


def main(args):
    url = _create_url(args)

    report(url, None)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create a highlight report for particular match.")
    parser.add_argument("-r", "--region", action="store_true", help="Region used to retrieve timeline file")
    parser.add_argument("-i", "--game-id", action="store_true", help="Game Id used to retrieve timeline file")
    parser.add_argument("-s", "--game-hash", action="store_true", help="Game Hash used to retrieve timeline file")
    parser.add_argument("-f", "--full-url", action="store_true", help="Full URL used to retrieve timeline file")

    args = parser.parse_args()
    main(args)
