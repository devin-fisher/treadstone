#!/usr/bin/env python
import requests
import json
import argparse

def kill_list_function(data):
    kill_list = []
    t = len(data['frames'])
    for x in range (0, t):

        z = len(data['frames'][x]['events'])
        y = 0
        v = 0
        for y in range (0, z):
            check = data['frames'][x]['events'][y]['type']
            if check == 'CHAMPION_KILL':

                kill = int(data['frames'][x]['events'][y]['timestamp'])
                time_seconds = (kill / 1000) % 60
                time_minutes = ((kill / 1000) - time_seconds) / 60
                #print(int (time_minutes),':', int (time_seconds), 'Champion Kill')
                if (time_seconds < 15):
                    time_minutes1 = time_minutes - 1
                    time_seconds1 = 60 - (8 - time_seconds)
                    #print(int (time_minutes1),':', int (time_seconds1))
                else:
                    g = 1
                    #print(int (time_minutes),':', int (time_seconds - 8))
                if (time_seconds > 58):
                    time_minutes2 = time_minutes + 1
                    time_seconds2 = (time_seconds + 2) - 60
                    #print(int (time_minutes2),':', int (time_seconds2))
                else:
                    g = 1
                    #print(int (time_minutes),':', int (time_seconds + 2))
                v = v + 1
                kill_list.append(kill)


            if check == 'BUILDING_KILL':

                kill = int(data['frames'][x]['events'][y]['timestamp'])
                time_seconds = (kill / 1000) % 60
                time_minutes = ((kill / 1000) - time_seconds) / 60
                #print(int (time_minutes),':', int (time_seconds),'Building_Kill')
                if (time_seconds < 5):
                    time_minutes1 = time_minutes - 1
                    time_seconds1 = 60 - (5 - time_seconds)
                    #print(int (time_minutes1),':', int (time_seconds1))
                else:
                    g =1
                    #print(int (time_minutes),':', int (time_seconds - 5))
                if (time_seconds > 58):
                    time_minutes2 = time_minutes + 1
                    time_seconds2 = (time_seconds + 2) - 60
                    #print(int (time_minutes2),':', int (time_seconds2))
                else:
                    g =1
                    #print(int (time_minutes),':', int (time_seconds + 2))
                v = v + 1
                kill_list.append(kill)

            if check == 'ELITE_MONSTER_KILL':

                kill = int(data['frames'][x]['events'][y]['timestamp'])
                time_seconds = (kill / 1000) % 60
                time_minutes = ((kill / 1000) - time_seconds) / 60
                #print(int (time_minutes),':', int (time_seconds),'Elite Monster Kill')
                if (time_seconds < 10):
                    time_minutes1 = time_minutes - 1
                    time_seconds1 = 60 - (10 - time_seconds)
                    #print(int (time_minutes1),':', int (time_seconds1))
                else:
                    g = 1
                    #print(int (time_minutes),':', int (time_seconds - 10))
                if (time_seconds > 55):
                    time_minutes2 = time_minutes + 1
                    time_seconds2 = (time_seconds + 5) - 60
                    #print(int (time_minutes2),':', int (time_seconds2))
                else:
                    g =1
                    #print(int (time_minutes),':', int (time_seconds + 5))
                v = v + 1
                kill_list.append(kill)
    y = y + 1
    x = x + 1
    new_list = []
    a = 0


    return kill_list

def start_counter_list_function(kill_list, counter_list):
    start_list = []

    kill_counter = 0
    kill_length = len(kill_list)
    start_list.append(kill_list[0])
    for a in range(1,kill_length):
        current = kill_list[a]
        last = a - 1
        before = kill_list[last]
        delta = current - before
        if delta > 15000:
            cur = kill_list[a]
            start_list.append(cur)
            counter_list.append(kill_counter)
            kill_counter  = 0
        else:
            kill_counter = kill_counter + 1
    counter_list.append(kill_counter)

    return start_list, counter_list

def end_list_function(kill_list, counter_list, start_list):
    end_list = []
    b = 0
    len_start_list = len(start_list)
    for a in range(0,len_start_list):
        end_counter = a + b + counter_list[a]
        end_list.append(kill_list[end_counter])
        b = b + counter_list[a]

    return end_list, counter_list

def report(start_list, end_list, data, team_fight):
    len_start_list = len(start_list)
    video_length = 0
    infographic_list = infographic_time_list_builder(data, team_fight)
    for a in range(0, len_start_list):
        time_seconds_start = int((start_list[a] / 1000) % 60)
        time_minutes_start = int(((start_list[a] / 1000) - time_seconds_start) / 60)
        if (time_seconds_start < 7):
            time_minutes_start = time_minutes_start - 1
            time_seconds_start = 60 - (7 - time_seconds_start)
        else:
            time_seconds_start = time_seconds_start - 7
        time_seconds_end = int((end_list[a] / 1000) % 60)
        time_minutes_end = int(((end_list[a] / 1000) - time_seconds_end) / 60)
        if (time_seconds_end > 57):
            time_minutes_end = time_minutes_end + 1
            time_seconds_end = (time_seconds_end + 3) - 60
        else:
            time_seconds_end = time_seconds_end + 3

        if (time_minutes_start == time_minutes_end):
            video_length = video_length + (time_seconds_end - time_seconds_start)
        else:
            video_length = video_length + ((60 - time_seconds_start) + time_seconds_end)


        len_infographic = len(infographic_list)
        c = 0
        for b in range(0,len_infographic):
            check = infographic_list[b]
            if check > (((time_minutes_start*60) + time_seconds_start)*1000) and check < (((time_minutes_end * 60) + time_seconds_end)*1000):
                if c == 0:
                    print("Infographic Needed")
                    c = 1
        print('start',time_minutes_start,':', time_seconds_start)
        print('end  ',time_minutes_end,':', time_seconds_end)
    print(int(video_length / 60),'Minutes and',video_length % 60,'Seconds')

def large_fight_function(start_list, counter_list):
    len_counter_list = len(counter_list)
    team_fight = []
    for a in range(0,len_counter_list):
        if (counter_list[a] >= 3):
            time_seconds_start = int((start_list[a] / 1000) % 60)
            time_minutes_start = int(((start_list[a] / 1000) - time_seconds_start) / 60)
            team_fight.append(start_list[a])
            print('Team Fights!!',time_minutes_start,':',time_seconds_start)

    return(team_fight)

def infographic_time_list_builder(data,team_fight):
    infographic_time_list = []
    len_game = len(data['frames']) // 5
    len_team_fight = len(team_fight)
    time_counter = 0
    for a in range(0,len_game):
        time_counter = time_counter + 5
        infographic_time = (time_counter * 60) * 1000
        infographic_time_list.append(infographic_time)
        for b in range(0,len_team_fight):
            team_fight_time = int((team_fight[b]/60)/1000)

            if team_fight_time > time_counter and team_fight_time < (time_counter + 5):
                infographic_time_list.append(team_fight[b])

    return(infographic_time_list)

def _create_url(args):
    return "https://acs.leagueoflegends.com/v1/stats/game/TRLH1/1001770122/timeline?gameHash=b49ec7b6e70e0ac3"

def main(args):
    url = _create_url(args)
    r = requests.get(url)
    data = r.json()
    counter_list = []
    kill_list = kill_list_function(data)
    start_list, counter_list = start_counter_list_function(kill_list, counter_list)
    end_list, counter_list = end_list_function(kill_list, counter_list, start_list)
    team_fight = large_fight_function(start_list, counter_list)
    report(start_list, end_list, data, team_fight)

    # print(kill_list)
    # print(start_list)
    # print(counter_list)
    # print(end_list)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create a highlight report for particular match.")
    parser.add_argument("-r", "--region", action="store_true", help="Region used to retrieve timeline file")
    parser.add_argument("-i", "--game-id", action="store_true", help="Game Id used to retrieve timeline file")
    parser.add_argument("-s", "--game-hash", action="store_true", help="Game Hash used to retrieve timeline file")
    parser.add_argument("-f", "--full-url", action="store_true", help="Full URL used to retrieve timeline file")

    args = parser.parse_args()
    main(args)
