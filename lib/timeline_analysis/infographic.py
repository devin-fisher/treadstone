from lib.util.http_lol_static import request_json_resource
from collections import OrderedDict
import math
from lib.timeline_analysis.timeline_lib import kill_list_function
from lib.timeline_analysis.timeline_lib import start_counter_list_function
from lib.timeline_analysis.timeline_lib import end_list_function
from lib.timeline_analysis.timeline_lib import large_fight_function
from lib.util.static_lol_data import get_champ_data


def player_gold(data, team_fight,time):
    player_gold_list = []
    len_team_fight = len(team_fight)
    time_stamp = int((time)/60)
    for b in range(1,11):
        x = str(b)
        player_gold = data['frames'][time_stamp]['participantFrames'][x]['totalGold']
        player_gold_list.append(player_gold)

    return(player_gold_list)

def player_items(data, team_fight, time):
    player_items_list = OrderedDict()
    data_len = len(data['frames'])
    len_team_fight = len(team_fight)
    time_stamp = int((time)/60)
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
                if check == 'ITEM_SOLD':
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

        health_potion = 2003
        vision_ward = 2043
        biscuit = 2010
        counter = 0
        for b in range(0,len(player_items_list1)):
            if player_items_list1[b] == biscuit:
                counter = counter + 1
        for c in range(0, counter - 1):
            player_items_list1.remove(biscuit)

        counter = 0
        for b in range(0,len(player_items_list1)):
            if player_items_list1[b] == health_potion:
                counter = counter + 1
        for c in range(0, counter - 1):
            player_items_list1.remove(health_potion)

        counter = 0
        for b in range(0,len(player_items_list1)):
            if player_items_list1[b] == vision_ward:
                counter = counter + 1
        for c in range(0, counter - 1):
            player_items_list1.remove(vision_ward)


        for b in range(0,len(player_items_list1)):
            if len(player_items_list1) < 4:
                check =  4 - len(player_items_list1)
                for c in range(0,check):
                    player_items_list1.append(0)
            if player_items_list1[b] == 3340:
                temp = player_items_list1[3]
                player_items_list1[3] = player_items_list1[b]
                player_items_list1[b] = temp

            if player_items_list1[b] == 3363:
                temp = player_items_list1[3]
                player_items_list1[3] = player_items_list1[b]
                player_items_list1[b] = temp

            if player_items_list1[b] == 3341:
                temp = player_items_list1[3]
                player_items_list1[3] = player_items_list1[b]
                player_items_list1[b] = temp

            if player_items_list1[b] == 3364:
                temp = player_items_list1[3]
                player_items_list1[3] = player_items_list1[b]
                player_items_list1[b] = temp

        # player_items_list[c][a] = player_items_list1
        player_items_list[a]['items'] = player_items_list1

    return player_items_list

def team_kills(data,time):
    time_stamp = int((time)/60)
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
    time_stamp = int((time)/60)
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
    time_stamp = int((time)/60)
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
    time_stamp = int((time)/60)
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
    time_stamp = int((time)/60)
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

def infographic_time_list_builder(data,team_fight, start_list):
    infographic_time_list = [0]
    test_list = []
    len_game = ((len(data['frames']) - 1) // 5)
    len_team_fight = len(team_fight)
    time_counter = 0
    for a in range(0,len_game):
        time_counter = time_counter + 5
        infographic_time = (time_counter * 60)
        test = True
        test_list.append(infographic_time)

        for b in range(0, len(start_list)):
            if start_list[b] - infographic_time > 0 :
                if test == True and infographic_time_list[a] != start_list[b]:
                    infographic_time_list.append(start_list[b])
                    test = False

        for c in range(0,len_team_fight):
            team_fight_time = int((team_fight[c]/60))
            if team_fight_time > time_counter and team_fight_time < (time_counter + 5) and team_fight[c] != infographic_time_list[a+1]:
                infographic_time_list.append((team_fight[c]))

    infographic_time_list.remove(0)
    # print(infographic_time_list)
    return(infographic_time_list)

def champion_id_list(data_stats):
    champion = []
    for a in range (0,10):
        champion_id = data_stats['participants'][a]['championId']
        champion.append(champion_id)

    return champion

def graph_info_red(data,time):
    time_stamp = int((time)/60)

    red_graph_list = []
    for a in range(0,time_stamp + 1):
        count_red = 0
        for c in range(6,11):
            count_red = count_red + data['frames'][a]['participantFrames'][str(c)]['totalGold']
        red_graph_list.append(count_red)
    return red_graph_list

def graph_info_blue(data,time):
    time_stamp = int((time)/60)
    blue_graph_list = []
    for a in range(0,time_stamp + 1):
        count_blue = 0
        for b in range(1,6):
            count_blue = count_blue + data['frames'][a]['participantFrames'][str(b)]['totalGold']
        blue_graph_list.append(count_blue)


    return blue_graph_list

def summoner_spell(data_stats):
    spell_list = []
    for a in range (0,10):
        spells = []
        spell_1 = data_stats['participants'][a]['spell1Id']
        spell_2 = data_stats['participants'][a]['spell2Id']
        spells.append(spell_1)
        spells.append(spell_2)
        spell_list.append(spells)

    return spell_list

def minion_count(data,time):
    minion_list = []
    time_stamp = int((time)/60)
    for b in range(1,11):
        x = str(b)
        minion = data['frames'][time_stamp]['participantFrames'][x]['minionsKilled']
        jungle = data['frames'][time_stamp]['participantFrames'][x]['jungleMinionsKilled']
        total_minion = minion + jungle
        minion_list.append(total_minion)

    return(minion_list)

def exp_lvl(data,time):
    exp_list = []
    time_stamp = int((time)/60) + 1
    for b in range(1,11):
        lvl_count = 0
        for a in range(0, time_stamp):
            for c in range(0, len(data['frames'][a]['events'])):
                check =  data['frames'][a]['events'][c]['type']
                if check == "SKILL_LEVEL_UP":
                    check2 = data['frames'][a]['events'][c]['participantId']
                    if check2 == b:

                        lvl_count = lvl_count + 1
        # print(lvl_count)

        exp_list.append(lvl_count)

    print(exp_list)
    print("--------")
    return(exp_list)

def lvl_stat_gold(champion_list,data,time):
    gold_efficiency = {"mpregenperlevel":5 , "attackspeedperlevel":25, "spellblockperlevel":18,"critperlevel":40, "hpperlevel":2.6, "hpregenperlevel":3, "attackdamageperlevel":35, "armorperlevel":20, "mpperlevel":1.4}
    lvl_stat_gold = []
    champion1 = get_champ_data("6.22.1", "Malphite")
    champion2 = get_champ_data("6.22.1", "Irelia")
    exp_list = exp_lvl(data,time)
    for a in range(0,5):
        total = 0
        lvl_difference = 0
        lvl_champ1 = 0
        lvl_champ2 = 0
        lvl_champ1 = exp_list[a]
        lvl_champ2 = exp_list[a+5]
        # print(lvl_difference)
        if lvl_champ1 > lvl_champ2:
            lvl_difference = lvl_champ1 - lvl_champ2
            total = total + (lvl_difference * (champion1["mpregenperlevel"] * gold_efficiency["mpregenperlevel"]))
            total = total + (lvl_difference * (champion1["attackspeedperlevel"] * gold_efficiency["attackspeedperlevel"]))
            total = total + (lvl_difference * (champion1["spellblockperlevel"] * gold_efficiency["spellblockperlevel"]))
            total = total + (lvl_difference * (champion1["critperlevel"] * gold_efficiency["critperlevel"]))
            total = total + (lvl_difference * (champion1["hpperlevel"] * gold_efficiency["hpperlevel"]))
            total = total + (lvl_difference * (champion1["hpregenperlevel"] * gold_efficiency["hpregenperlevel"]))
            total = total + (lvl_difference * (champion1["attackdamageperlevel"] * gold_efficiency["attackdamageperlevel"]))
            total = total + (lvl_difference * (champion1["armorperlevel"] * gold_efficiency["armorperlevel"]))
            total = total + (lvl_difference * (champion1["mpperlevel"] * gold_efficiency["mpperlevel"]))
            # print(total)
        elif lvl_champ1 < lvl_champ2:
            lvl_difference = lvl_champ2 - lvl_champ1
            # for b in range(0,len(champion1)):
            total = total - (lvl_difference * (champion2["mpregenperlevel"] * gold_efficiency["mpregenperlevel"]))
            total = total - (lvl_difference * (champion2["attackspeedperlevel"] * gold_efficiency["attackspeedperlevel"]))
            total = total - (lvl_difference * (champion2["spellblockperlevel"] * gold_efficiency["spellblockperlevel"]))
            total = total - (lvl_difference * (champion2["critperlevel"] * gold_efficiency["critperlevel"]))
            total = total - (lvl_difference * (champion2["hpperlevel"] * gold_efficiency["hpperlevel"]))
            total = total - (lvl_difference * (champion2["hpregenperlevel"] * gold_efficiency["hpregenperlevel"]))
            total = total - (lvl_difference * (champion2["attackdamageperlevel"] * gold_efficiency["attackdamageperlevel"]))
            total = total - (lvl_difference * (champion2["armorperlevel"] * gold_efficiency["armorperlevel"]))
            total = total - (lvl_difference * (champion2["mpperlevel"] * gold_efficiency["mpperlevel"]))
            # print(total)
        else:
            total = 0
        # print(total)
        lvl_stat_gold.append(total)


    return(lvl_stat_gold)


def power_index(data, time):
    time_stamp = int((time)/60)
    print(time_stamp)
    max_gold_diff = 5000
    power_index_list = []
    champion_list = []
    lvl_gold = lvl_stat_gold(champion_list,data,time)
    exp_list = exp_lvl(data,time)
    for a in range(1,6):
        total_gold = 0
        gold_spent1 = 0
        gold_spent2 = 0
        gold_difference = 0
        index = 0
        x = str(a)
        z = str(a+5)
        y = a -1
        gold_spent1 = data['frames'][time_stamp]['participantFrames'][x]['totalGold'] - data['frames'][time_stamp]['participantFrames'][x]['currentGold']
        gold_spent2 = data['frames'][time_stamp]['participantFrames'][z]['totalGold'] - data['frames'][time_stamp]['participantFrames'][z]['currentGold']
        gold_difference = gold_spent1 - gold_spent2
        # print(gold_difference)
        if gold_spent1 > gold_spent2:
            total_gold = gold_difference + lvl_gold[y]
            print(total_gold)
        elif gold_spent1 < gold_spent2:
            total_gold = gold_difference - lvl_gold[y]
            print(total_gold)
        else:  # Gold is equal
            total_gold = lvl_gold[y]
            print(total_gold)
        if abs(total_gold) > 4000:
            if total_gold > 0:
                total_gold = 2*(math.sqrt(pow(total_gold,2)+5000*total_gold)-total_gold)
            if total_gold < 0:
                total_gold = -(total_gold)
                total_gold = -(2*(math.sqrt(pow(total_gold,2)+5000*total_gold)-total_gold))
            else:
                total_gold = total_gold
        if exp_list[a-1] > 10 or exp_list[a+4] > 10:
            total_gold = total_gold * .75
        if total_gold > 0:
            index = total_gold / max_gold_diff
        if total_gold < 0:
            index = (0 - (abs(total_gold) / max_gold_diff))
        index = int(index * 100)
        power_index_list.append(index)
        # print(total_gold)

    print(exp_list)

    print(power_index_list)
    print("-----------")
    return(power_index_list)

def infographic_list_builder(url,url_stats):

    data = request_json_resource(url)
    stats_data = request_json_resource(url_stats)
    # r = requests.get(url)
    # s = requests.get(url_stats)
    # data = r.json()
    # data_stats = s.json()

    counter_list = []
    kill_list = kill_list_function(data,stats_data)
    start_list, counter_list = start_counter_list_function(kill_list, counter_list)
    end_list, counter_list = end_list_function(kill_list, counter_list, start_list)
    team_fight = large_fight_function(start_list, counter_list)
    champion_list = champion_id_list(stats_data)
    spell_list = summoner_spell(stats_data)


    infographic_time_list = infographic_time_list_builder(data, team_fight, start_list)
    len_infographic_time_list = len(infographic_time_list)
    print(infographic_time_list)
    infographic_list = []
    time = infographic_time_list[1]
    champ = "aatrox"



    for a in range(0,len_infographic_time_list):
        a_index = a
        # a = str(a)
        time = infographic_time_list[a]
        player_gold_list = player_gold(data,team_fight,time)
        player_items_list = player_items(data, team_fight, time)
        kill_score = team_kills(data, time)
        tower_score = team_towers(data,time)
        team_gold_list = team_gold(player_gold_list)
        player_kill_list = player_kills(data,time)
        player_assist_list = player_assists(data,time)
        player_death_list = player_deaths(data,time)
        dragon_count_list = dragon_counter(data,time)
        minion_list = minion_count(data,time)
        lvl_list = exp_lvl(data,time)
        index = power_index(data,time)

        blue_graph_list = graph_info_blue(data,time)
        blue_player_kill_list = player_kill_list[0:5]
        blue_player_death_list = player_death_list[0:5]
        blue_player_gold_list = player_gold_list[0:5]
        blue_player_assist_list = player_assist_list[0:5]
        blue_champion_list = champion_list[0:5]
        blue_spell_list = spell_list[0:5]
        blue_minion_list = minion_list[0:5]
        blue_lvl_list = lvl_list[0:5]

        team_1 = 0
        team_2 = 1
        infographic_list.append([])
        infographic_list[a].append(OrderedDict())
        infographic_list[a].append(OrderedDict())

        infographic_list[a][team_1]["timeStamp"] = infographic_time_list[a_index]
        infographic_list[a][team_1]["teamGold"] = team_gold_list[1]
        infographic_list[a][team_1]["teamKills"] = kill_score[0]
        infographic_list[a][team_1]["towerKills"] = tower_score[0]
        infographic_list[a][team_1]["dragonKills"] = dragon_count_list[1]
        infographic_list[a][team_1]["playerKills"] = blue_player_kill_list
        infographic_list[a][team_1]["playerAssists"] = blue_player_assist_list
        infographic_list[a][team_1]["playerDeaths"] = blue_player_death_list
        infographic_list[a][team_1]["playerGold"] = blue_player_gold_list
        infographic_list[a][team_1]["championId"] = blue_champion_list
        infographic_list[a][team_1]["totalGoldGraph"] = blue_graph_list
        infographic_list[a][team_1]["summonerSpell"] = blue_spell_list
        infographic_list[a][team_1]["minionsKilled"] = blue_minion_list
        infographic_list[a][team_1]["playerLevel"] = blue_lvl_list

        infographic_list[a][team_1]['playerItem'] = []
        for b in range(1,6):
            infographic_list[a][team_1]['playerItem'].append(player_items_list[b]['items'])
        infographic_list[a][team_1]['power'] = index

        red_graph_list = graph_info_red(data,time)
        red_player_kill_list = player_kill_list[5:10]
        red_player_death_list = player_death_list[5:10]
        red_player_gold_list = player_gold_list[5:10]
        red_player_assist_list = player_assist_list[5:10]
        red_champion_list = champion_list[5:11]
        red_spell_list = spell_list[5:11]
        red_minion_list = minion_list[5:11]
        red_lvl_list = lvl_list[0:5]

        infographic_list[a][team_2]["timeStamp"] = infographic_time_list[a_index]
        infographic_list[a][team_2]['teamGold'] = team_gold_list[2]
        infographic_list[a][team_2]['teamKills'] = kill_score[1]
        infographic_list[a][team_2]['towerKills'] = tower_score[1]
        infographic_list[a][team_2]['dragonKills'] = dragon_count_list[2]
        infographic_list[a][team_2]['playerKills'] = red_player_kill_list
        infographic_list[a][team_2]["playerAssists"] = red_player_assist_list
        infographic_list[a][team_2]['playerDeaths'] = red_player_death_list
        infographic_list[a][team_2]['playerGold'] = red_player_gold_list
        infographic_list[a][team_2]['championId'] = red_champion_list
        infographic_list[a][team_2]['totalGoldGraph'] = red_graph_list
        infographic_list[a][team_2]['summonerSpell'] = red_spell_list
        infographic_list[a][team_2]['minionsKilled'] = red_minion_list
        infographic_list[a][team_2]["playerLevel"] = red_lvl_list

        infographic_list[a][team_2]['playerItem'] = []
        for b in range(6,11):
            infographic_list[a][team_2]['playerItem'].append(player_items_list[b]['items'])

        infographic_list[a][team_2]['power'] = index
    # print(infographic_list)
    return(infographic_list)

