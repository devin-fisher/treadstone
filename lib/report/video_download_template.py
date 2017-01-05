standard_command = "echo Downloading %(game_name)s:\r\nyoutube-dl "\
"-f bestvideo[ext=mp4]+bestaudio[ext=m4a]/bestvideo+bestaudio "\
"--merge-output-format mp4 " \
"-o '%(game_name)s_full_game_video.mp4' " \
"%(youtube_url)s"

def video_download_batch_file(game_list):
    rtn = "@echo off\r\n\r\n"
    for game_info in game_list:
        rtn += standard_command % game_info
        rtn += "\r\n"
    return rtn
