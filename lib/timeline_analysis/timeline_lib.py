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
