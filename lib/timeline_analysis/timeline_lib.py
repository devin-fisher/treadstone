from collections import OrderedDict

def kill_list_function(data,stats_data):
    kill_list = []
    t = len(data['frames'])
    game_length = stats_data['gameDuration'] - 3
    b = 0
    for x in range (0, t):

        z = len(data['frames'][x]['events'])
        y = 0
        v = 0

        for y in range (0, z):


            check = data['frames'][x]['events'][y]['type']

            if check == 'CHAMPION_KILL':

                kill_list.append({})
                kill = int(data['frames'][x]['events'][y]['timestamp'])
                kill1 = int(kill/1000)
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
                killer = int(data['frames'][x]['events'][y]['killerId'])
                victim = int(data['frames'][x]['events'][y]['victimId'])
                assist = data['frames'][x]['events'][y]['assistingParticipantIds']
                participants = []
                participants.append(killer)
                participants.append(victim)

                for a in range(0,len(assist)):
                    participants.append(assist[a])


                kill_list[b]["time"] = kill1
                kill_list[b]["eventType"] = 'CHAMPION_KILL'
                kill_list[b]["participants"] = participants

                b = b + 1

            if check == 'BUILDING_KILL':
                kill_list.append({})
                kill = int(data['frames'][x]['events'][y]['timestamp'])
                kill1 = int(kill/1000)
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

                killer = int(data['frames'][x]['events'][y]['killerId'])
                building_type = data['frames'][x]['events'][y]['buildingType']
                tower = data['frames'][x]['events'][y]['towerType']
                if (tower == "BASE_TURRET" or tower == "NEXUS_TURRET" or tower == "UNDEFINED_TURRET"):
                    tower_type = "BASE_TURRET"
                else:
                    tower_type = "OUTER_TURRET"


                kill_list[b]["time"] = kill1
                kill_list[b]["eventType"] = 'BUILDING_KILL'
                kill_list[b]["towerType"] = tower_type

                b = b + 1

            if check == 'ELITE_MONSTER_KILL':

                kill_list.append({})
                kill = int(data['frames'][x]['events'][y]['timestamp'])
                kill1 = int(kill/1000)
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
                killer = int(data['frames'][x]['events'][y]['killerId'])
                monster_type = data['frames'][x]['events'][y]['monsterType']



                kill_list[b]["time"] = kill1
                kill_list[b]["eventType"] = 'MONSTER_KILL'
                kill_list[b]["monsterKill"] = monster_type
                kill_list[b]["killerID"] = killer

                b = b + 1

    y = y + 1
    x = x + 1
    new_list = []
    a = 0
    last_item = {}
    last_item['time'] = game_length
    last_item['eventType'] = "NEXUS_KILL"

    kill_list.append(last_item)


    return kill_list

def start_counter_list_function(kill_list, counter_list):
    start_list = [{}]
    counter_list = []
    kill_counter = 0
    kill_length = len(kill_list)
    start_list[0] = kill_list[0]
    for a in range(1,kill_length):
        kill_time = kill_list[a]['time']

        current = int(kill_list[a]['time'])
        last = a - 1
        before = int(kill_list[last]["time"])
        delta = current - before
        if delta > 15:
            cur = int(kill_list[a]["time"])
            start_list.append(kill_list[a])
            counter_list.append(kill_counter)
            kill_counter = 0
        else:
            kill_counter = kill_counter + 1
            # start_list.append(kill_list[a])
    counter_list.append(kill_counter)

    return start_list, counter_list

def end_list_function(kill_list, counter_list, start_list):
    end_list = []
    b = 0
    len_start_list = len(start_list)
    for a in range(0,len_start_list):
        end_counter = a + b + counter_list[a]
        end_list.append({})
        end_list[a]['time'] = kill_list[end_counter]["time"]
        end_list[a]['eventType'] = kill_list[end_counter]["eventType"]
        b = b + counter_list[a]

    return end_list, counter_list

def large_fight_function(start_list, counter_list):
    len_counter_list = len(counter_list)
    team_fight = []
    for a in range(0,len_counter_list):
        if (counter_list[a] >= 3):
            time_seconds_start = int((start_list[a]['time']) % 60)
            time_minutes_start = int(((start_list[a]['time']) - time_seconds_start) / 60)
            team_fight.append(start_list[a]['time'])
            # print('Team Fights!!',time_minutes_start,':',time_seconds_start)
    return(team_fight)
