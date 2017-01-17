import os
import json


def roster(team):
    team1 = [0, 0, 0, 0, 0]
    team2 = [0, 0, 0, 0, 0]
    for a in range(0,5):
        player = team['teams'][0]['starters'][a]
        for b in range(0, len(team['players'])):
            check = team['players'][b]['id']
            if player == check:
                role = team['players'][b]['roleSlug']
        if role == "toplane":
            team1[0] = player
        if role == "jungle":
            team1[1] = player
        if role == "midlane":
            team1[2] = player
        if role == "adcarry":
            team1[3] = player
        if role == "support":
            team1[4] = player
    for a in range(0,5):
        player = team['teams'][1]['starters'][a]
        for b in range(0, len(team['players'])):
            check = team['players'][b]['id']
            if player == check:
                role = team['players'][b]['roleSlug']
        if role == "toplane":
            team2[0] = player
        if role == "jungle":
            team2[1] = player
        if role == "midlane":
            team2[2] = player
        if role == "adcarry":
            team2[3] = player
        if role == "support":
            team2[4] = player
    rosters_rtn = list()
    rosters_rtn.append(team1)
    rosters_rtn.append(team2)

    return rosters_rtn


def title_info(schedule,team,match):
    # example: team1 vs team2: game# - day# week# splitseason year
    # Need NA and split
    team_title = team['teams'][0]['acronym'] + " vs " + team['teams'][1]['acronym']
    series_type = "Best of 3"
    day = 'Day ' + schedule['scheduleItems'][0]['tags']['subBlockLabel']
    week = 'Week ' + schedule['scheduleItems'][0]['tags']['blockLabel']
    split = match['tournament_description']
    title = team_title + ": " + series_type + " - " + day + " " + week + " " + split
    return title


def description(schedule,team,match):
    # example:
    # title and link to previous video
    # full game title again
    # team1 with all players full names and gameIDs
    # team2 with all players full names and gameIDs
    title = title_info(schedule,team,match)
    date = schedule['scheduleItems'][0]['scheduledTime']
    line1 = title
    line2 = "Date game was played: " + date[0:10]
    line3 = ""  # "Previous game: https://www.youtube.com/watch?v=s_49xu418aw&t=2s&list=PLVgS_BIOY01wO0VzCC2u54219cy9sKK-s&index=19"
    line4 = team['teams'][0]['acronym'] + " Roster"
    line5 = team['teams'][1]['acronym'] + " Roster"
    rosters = roster(team)
    roster_info = []
    for a in range(0, len(rosters)):
        for b in range(0, len(rosters[a])):
            for c in range(0,len(team['players'])):
                check = team['players'][c]['id']
                player_number = rosters[a][b]
                if player_number == check:
                    player_info = team['players'][c]['firstName'] + " '" + team['players'][c]['name'] + "' " + team['players'][c]['lastName']
                    roster_info.append(player_info)
    description_rtn = line1 + "#n#n" + line2 + "#n" + line3 + "#n#n" + line4 + "#n#n" + roster_info[0] + "#n" + roster_info[1] + "#n" + roster_info[2] + "#n" + roster_info[3] + "#n" + roster_info[4] + "#n#n" + line5 + "#n#n" + roster_info[5] + "#n" + roster_info[6] + "#n" + roster_info[7] + "#n" + roster_info[8] + "#n" + roster_info[9]

    return description_rtn


def category():
    category_rtn = "Gaming"
    return category_rtn


def tags(team, match):

    hard_tags = "League, League of Legends, LoL, LCS, League Championship Series, NALCS, EULCS, LCK, LPL, LMS, Esports"
    situational_tags = team['teams'][0]['acronym'] + ", " + team['teams'][1]['acronym'] + ", " + match['id']
    all_tags = hard_tags + ", " + situational_tags
    return all_tags


def default_language():
    default_language_rtn = "en"
    return default_language_rtn


def client_secrets():
    client_secrets_rtn = "C:\youtube_upload\youtube-upload-master\client_secrets.json"
    return client_secrets_rtn


def playlist(schedule, match):
    # need NA and split
    day = 'Day ' + schedule['scheduleItems'][0]['tags']['subBlockLabel']
    week = 'Week ' + schedule['scheduleItems'][0]['tags']['blockLabel']
    split = match['tournament_description']
    playlist_rtn = week + " " + split
    return playlist_rtn


def privacy():
    privacy_rtn = "public"
    return privacy_rtn


def upload_batch_file(schedule, team, match):
    title = title_info(schedule, team, match)
    descriptions = description(schedule, team, match)
    categories = category()
    client = client_secrets()
    playlists = playlist(schedule, match)
    privacy_info = privacy()
    video_name = "intro_final.mp4"
    tag = tags(team,match)
    #test = """youtube-upload --title="IMT vs APX" --description="IMT vs APX" --category=Gaming --client-secrets=C:\youtube_upload\youtube-upload-master\client_secrets.json E:\Youtube\Test/test_export.mp4"""
    content = "youtube-upload --title=\"" + title + "\" --description=\"" + descriptions + "\" --tags=\"" + tag + "\" --category=" + categories + " --client-secrets=" + client + " --playlist=\"" + playlists + "\" --privacy=" + privacy_info + " " + video_name
    # print(content)
    # directory = 'E:/Youtube/Test/game/'
    # with open(os.path.join(directory, 'match-video-upload.bat'), 'w') as OPATH:
    #      OPATH.writelines(['@echo off \n',
    #                          'echo Uploading Match:',
    #                        '\n',
    #                        content])
    return """
@echo off
echo Uploading Match:

""" + content


def main():
    with open('E:\Youtube\Test\game\schedule_info.json') as json_data:
        r = json.load(json_data)
        json_data.close()
    schedule = r
    with open(r'E:\Youtube\Test\game\team_info.json') as json_data:
        s = json.load(json_data)
        json_data.close()
    team = s
    with open(r'E:\Youtube\Test\game\match_info.json') as json_data:
        t = json.load(json_data)
        json_data.close()
    match = t
    upload_batch_file(schedule, team, match)
    # upload()

if __name__ == "__main__":
    main()