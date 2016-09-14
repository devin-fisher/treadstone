import json
import argparse
from lib.util.http_lol_static import request_json_resource
from collections import OrderedDict

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

def large_fight_function(start_list, counter_list):
    len_counter_list = len(counter_list)
    team_fight = []
    for a in range(0,len_counter_list):
        if (counter_list[a] >= 3):
            time_seconds_start = int((start_list[a] / 1000) % 60)
            time_minutes_start = int(((start_list[a] / 1000) - time_seconds_start) / 60)
            team_fight.append(start_list[a])
            # print('Team Fights!!',time_minutes_start,':',time_seconds_start)

    return(team_fight)

def _create_url(args):
    return "https://acs.leagueoflegends.com/v1/stats/game/TRLH1/1001770122/timeline?gameHash=b49ec7b6e70e0ac3"

def player_gold(data, team_fight,time):
    player_gold_list = []
    len_team_fight = len(team_fight)
    time_stamp = int((time/1000)/60)
    for b in range(1,11):
        x = str(b)
        player_gold = data['frames'][time_stamp]['participantFrames'][x]['totalGold']
        player_gold_list.append(player_gold)

    return(player_gold_list)

def player_items(data, team_fight, time):
    player_items_list = OrderedDict()
    data_len = len(data['frames'])
    len_team_fight = len(team_fight)
    time_stamp = int((time/1000)/60)
    for a in range(1,11):
        player_id = a
        player_items_list[a] = OrderedDict()
        player_items_list1 = []
        for x in range (0, time_stamp):
            z = len(data['frames'][x]['events'])
            for y in range (0, z):
                check = data['frames'][x]['events'][y]['type']
                item_id = 0
                if check == "ITEM_PURCHASED":
                    check2 = data['frames'][x]['events'][y]['participantId']
                    if check2 == player_id:
                        item_id = data['frames'][x]['events'][y]['itemId']
                        player_items_list1.append(item_id)
                if check == 'ITEM_UNDO':
                    check2 = data['frames'][x]['events'][y]['participantId']
                    check3 = data['frames'][x]['events'][y]['afterId']
                    if check2 == player_id:
                        if check3 != 0:
                            item_id = data['frames'][x]['events'][y]['afterId']
                            # player_items_list1.remove(item_id)
                            # print('Item Undo After', item_id)
                        else:
                            item_id = data['frames'][x]['events'][y]['beforeId']
                            player_items_list1.remove(item_id)

        for x in range (0, time_stamp):
            z = len(data['frames'][x]['events'])
            for y in range (0, z):
                check = data['frames'][x]['events'][y]['type']
                if check == 'ITEM_DESTROYED':
                    check2 = data['frames'][x]['events'][y]['participantId']
                    if check2 == player_id:
                        item_id = data['frames'][x]['events'][y]['itemId']
                        if item_id == 3200:
                            player_items_list1.append(item_id)
                        quit = 0
                        for c in range(0,len(player_items_list1)):
                            check4 = player_items_list1[c]
                            if check4 == item_id:
                                quit = 1
                        if quit == 1:
                            player_items_list1.remove(item_id)

        # player_items_list[c][a] = player_items_list1
        player_items_list[a]['items'] = player_items_list1

    return player_items_list

def team_kills(data,time):
    time_stamp = int((time/1000)/60)
    count_red = 0
    count_blue = 0
    kill_score = [1,2]
    for x in range (0, time_stamp):
        z = len(data['frames'][x]['events'])
        y = 0
        for y in range (0, z):
            check = data['frames'][x]['events'][y]['type']
            if check == 'CHAMPION_KILL':
                check2 = data['frames'][x]['events'][y]['killerId']
                if check2 <= 5:
                    count_blue = count_blue + 1
                else:
                    count_red = count_red + 1
    kill_score[0] = count_blue
    kill_score[1] = count_red
    return(kill_score)

def team_towers(data,time):
    time_stamp = int((time/1000)/60)
    count_red = 0
    count_blue = 0
    tower_score = [1,2]
    for x in range (0, time_stamp):
        z = len(data['frames'][x]['events'])
        y = 0
        for y in range (0, z):
            check = data['frames'][x]['events'][y]['type']
            if check == 'BUILDING_KILL':
                check2 = data['frames'][x]['events'][y]['buildingType']
                if check2 == 'TOWER_BUILDING':
                    check3 = data['frames'][x]['events'][y]['teamId']
                    if check3 == 200:
                        count_blue = count_blue + 1
                    else:
                        count_red = count_red + 1
    tower_score[0] = count_blue
    tower_score[1] = count_red

    return(tower_score)

def team_gold(player_gold_list):
    len_player_gold_list = len(player_gold_list)
    team_gold_list = OrderedDict()
    blue_gold = 0
    red_gold = 0
    for a in range(0, 5):
        blue_gold = blue_gold + player_gold_list[a]
    for b in range(5,10):
        red_gold = red_gold + player_gold_list[b]
    team_gold_list[1] = blue_gold
    team_gold_list[2] = red_gold

    return(team_gold_list)

def player_kills(data, time):
    time_stamp = int((time/1000)/60)
    player_kill_list = []
    for a in range(1,11):
        kill_count = 0
        for x in range (0, time_stamp):
            z = len(data['frames'][x]['events'])
            y = 0
            for y in range (0, z):
                check = data['frames'][x]['events'][y]['type']
                if check == 'CHAMPION_KILL':
                    check2 = data['frames'][x]['events'][y]['killerId']
                    if check2 == a:
                        kill_count = kill_count + 1
        player_kill_list.append(kill_count)

    return(player_kill_list)

def player_assists(data,time):
    time_stamp = int((time/1000)/60)
    player_assist_list = []
    for a in range(1,11):
        assist_count = 0
        for x in range (0, time_stamp):
            z = len(data['frames'][x]['events'])
            y = 0
            for y in range (0, z):
                check = data['frames'][x]['events'][y]['type']
                if check == 'CHAMPION_KILL':
                    check2 = data['frames'][x]['events'][y]['assistingParticipantIds']
                    len_check = len(check2)
                    for b in range(0,len_check):
                        check3 = check2[b]
                        if check3 == a:
                            assist_count = assist_count + 1
        player_assist_list.append(assist_count)

    return(player_assist_list)

def player_deaths(data, time):
    time_stamp = int((time/1000)/60)
    player_death_list = []
    for a in range(1,11):
        death_count = 0
        for x in range (0, time_stamp):
            z = len(data['frames'][x]['events'])
            y = 0
            for y in range (0, z):
                check = data['frames'][x]['events'][y]['type']
                if check == 'CHAMPION_KILL':
                    check2 = check = data['frames'][x]['events'][y]['victimId']
                    if check2 == a:
                        death_count = death_count + 1
        player_death_list.append(death_count)

    return(player_death_list)

def inhibitor_timer(data,time):
    t = len(data['frames'])
    inhib_status = OrderedDict()
    # inhib_status will have 3 values per inhibitor event. First is TRUE FALSE refering to Super Minions, Second is lane assignment, Third is time remaining until inhibitor restores
    status_list = []
    null_list = [0,0]
    count = 0
    count2 = 0
    lane = 0
    # lane assignments (1 = top, 2 = mid, 3 = bot)
    super_minions = 0
    # super_minions (0 = false, 1 = true)
    time_remaining = 0
    inhib_status[1] = OrderedDict()
    inhib_status[2] = OrderedDict()
    inhib_status[1][1] = null_list
    inhib_status[2][1] = null_list
    for x in range (0, t):
        z = len(data['frames'][x]['events'])
        lane = 0
        for y in range (0, z):
            status_list = []
            check = data['frames'][x]['events'][y]['type']
            if check == 'BUILDING_KILL':
                check2 = data['frames'][x]['events'][y]['buildingType']
                if check2 == 'INHIBITOR_BUILDING':
                    check3 = data['frames'][x]['events'][y]['timestamp']
                    if time >= check3 and time <= check3 + 300000:
                        time_remaining = 300000 - (time - check3)
                        super_minions = 1
                        status_list.append(super_minions)
                        if data['frames'][x]['events'][y]['laneType'] == 'TOP_LANE':
                            lane = 1
                        if data['frames'][x]['events'][y]['laneType'] == 'MID_LANE':
                            lane = 2
                        if data['frames'][x]['events'][y]['laneType'] == 'BOT_LANE':
                            lane = 3
                        status_list.append(lane)
                        status_list.append(time_remaining)
                        if data['frames'][x]['events'][y]['teamId'] == 100:
                            count = count + 1
                            inhib_status[1][count] = status_list
                        if data['frames'][x]['events'][y]['teamId'] == 200:
                            count2 = count2 + 1
                            inhib_status[2][count2] = status_list


    return(inhib_status)

def baron_timer(data,time):
    t = len(data['frames'])
    baron_buff = 0
    # baron_buff: This value refers to team (0 = neither 1 = blue 2 = red)
    for x in range (0, t):
        z = len(data['frames'][x]['events'])
        lane = 0
        for y in range (0, z):
            baron_list = []
            check = data['frames'][x]['events'][y]['type']
            if check == 'ELITE_MONSTER_KILL':
                check2 = data['frames'][x]['events'][y]['monsterType']
                if check2 == 'BARON_NASHOR':
                    check3 = data['frames'][x]['events'][y]['timestamp']
                    if time >= check3 and time <= check3 + 210000:
                        check4 = data['frames'][x]['events'][y]['killerId']
                        if check4 <= 5:
                            baron_buff = 1
                        if check4 > 5:
                            baron_buff = 2


    return(baron_buff)

def dragon_counter(data, time):
    time_stamp = int((time/1000)/60)
    dragon_count_list = OrderedDict()
    dragon_count_list[1] = OrderedDict()
    dragon_count_list[2] =OrderedDict()
    dragon_count_blue = 0
    dragon_count_red = 0
    for x in range (0, time_stamp):
        z = len(data['frames'][x]['events'])
        y = 0
        for y in range (0, z):
            check = data['frames'][x]['events'][y]['type']
            if check == 'ELITE_MONSTER_KILL':
                check2 = data['frames'][x]['events'][y]['monsterType']
                if check2 == 'DRAGON':
                    check3 = data['frames'][x]['events'][y]['killerId']
                    if check3 <= 5:
                        dragon_count_blue = dragon_count_blue + 1
                    if check3 >= 6:
                        dragon_count_red = dragon_count_red + 1

    dragon_count_list[1] = dragon_count_blue
    dragon_count_list[2] = dragon_count_red

    return(dragon_count_list)

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

def infographic_list_builder(url):
    data = request_json_resource(url)
    counter_list = []
    kill_list = kill_list_function(data)
    start_list, counter_list = start_counter_list_function(kill_list, counter_list)
    end_list, counter_list = end_list_function(kill_list, counter_list, start_list)
    team_fight = large_fight_function(start_list, counter_list)

    infographic_time_list = infographic_time_list_builder(data, team_fight)
    len_infographic_time_list = len(infographic_time_list)
    infographic_list = OrderedDict()

    for a in range(0,len_infographic_time_list):
        a_index = a
        a = str(a)
        time = infographic_time_list[a_index]

        player_gold_list = player_gold(data,team_fight,time)
        player_items_list = player_items(data, team_fight, time)
        kill_score = team_kills(data, time)
        tower_score = team_towers(data,time)
        team_gold_list = team_gold(player_gold_list)
        player_kill_list = player_kills(data,time)
        player_assist_list = player_assists(data,time)
        player_death_list = player_deaths(data,time)
        dragon_count_list = dragon_counter(data,time)

        blue_player_kill_list = player_kill_list[0:5]
        blue_player_death_list = player_death_list[0:5]
        blue_player_gold_list = player_gold_list[0:5]
        blue_player_assist_list = player_assist_list[0:5]


        team_1 = "100"
        team_2 = "200"
        infographic_list[a] = OrderedDict()
        infographic_list[a][team_1] = OrderedDict()
        infographic_list[a][team_2] = OrderedDict()

        infographic_list[a][team_1]["timeStamp"] = infographic_time_list[a_index]
        infographic_list[a][team_1]["teamGold"] = team_gold_list[1]
        infographic_list[a][team_1]["teamKills"] = kill_score[0]
        infographic_list[a][team_1]["towerKills"] = tower_score[0]
        infographic_list[a][team_1]["dragonKills"] = dragon_count_list[1]
        infographic_list[a][team_1]["playerKills"] = blue_player_kill_list
        infographic_list[a][team_1]["playerAssists"] = blue_player_assist_list
        infographic_list[a][team_1]["playerDeaths"] = blue_player_death_list
        infographic_list[a][team_1]["playerGold"] = blue_player_gold_list

        infographic_list[a][team_1]['playerItem'] = OrderedDict()
        for b in range(1,6):
            infographic_list[a][team_1]['playerItem'][b] = player_items_list[b]['items']


        red_player_kill_list = player_kill_list[5:10]
        red_player_death_list = player_death_list[5:10]
        red_player_gold_list = player_gold_list[5:10]
        red_player_assist_list = player_assist_list[5:10]

        infographic_list[a][team_2]["timeStamp"] = infographic_time_list[a_index]
        infographic_list[a][team_2]['teamGold'] = team_gold_list[2]
        infographic_list[a][team_2]['teamKills'] = kill_score[1]
        infographic_list[a][team_2]['towerKills'] = tower_score[1]
        infographic_list[a][team_2]['dragonKills'] = dragon_count_list[2]
        infographic_list[a][team_2]['playerKills'] = red_player_kill_list
        infographic_list[a][team_2]["playerAssists"] = red_player_assist_list
        infographic_list[a][team_2]['playerDeaths'] = red_player_death_list
        infographic_list[a][team_2]['playerGold'] = red_player_gold_list

        infographic_list[a][team_2]['playerItem'] = OrderedDict()
        for b in range(6,11):
            infographic_list[a][team_2]['playerItem'][b] = player_items_list[b]['items']


    # print(infographic_list)
    return(infographic_list)

def main(args):
    url = _create_url(args)
    infographic_list_builder(url)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create a highlight report for particular match.")
    parser.add_argument("-r", "--region", action="store_true", help="Region used to retrieve timeline file")
    parser.add_argument("-i", "--game-id", action="store_true", help="Game Id used to retrieve timeline file")
    parser.add_argument("-s", "--game-hash", action="store_true", help="Game Hash used to retrieve timeline file")
    parser.add_argument("-f", "--full-url", action="store_true", help="Full URL used to retrieve timeline file")

    args = parser.parse_args()
    main(args)
