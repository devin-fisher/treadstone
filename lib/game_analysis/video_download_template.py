standard_snipt = "echo Downloading %(game_name)s:\r\nyoutube-dl -f bestvideo+bestaudio" \
                 " -o '%(game_name)s_full_game_video.mp4'  %(youtube_url)s"


def video_download_batch_file(game_list):
    rtn = "@echo off\r\n\r\n"
    for game_info in game_list:
        rtn += standard_snipt % game_info
        rtn += "\r\n"
    return rtn
