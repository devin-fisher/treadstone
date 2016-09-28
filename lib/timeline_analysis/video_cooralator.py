from collections import OrderedDict
from lib.video.video_still_util import seconds_to_string

def _convert_millisec_to_sec(mil):
    if mil > 6000:
        return mil/1000
    else:
        return mil


def _find_video_time(video_breaks, game_time):
    cur_shift_video = video_breaks['start']
    cur_shift_game = 0
    game_time = _convert_millisec_to_sec(game_time)
    for video_break in video_breaks['shifts']:
        if game_time <= video_break['start_game_time']:
            rtn = cur_shift_video + (game_time - cur_shift_game)
            return rtn
        elif game_time <= video_break['end_game_time']:  # if the time is during the break
            raise Exception("Event is during break in video")
        else:
            cur_shift_video = video_break['start_time']
            cur_shift_game = video_break['start_game_time']
            pass

    return cur_shift_video + (game_time - cur_shift_game)


def video_event_translator(events, video_breaks):
    rtn = []
    for range_data in events:
        translated = OrderedDict()
        game_start = range_data['startTime']
        game_end = range_data['endTime']

        video_start = _find_video_time(video_breaks, range_data['startTime'])
        video_end = _find_video_time(video_breaks, range_data['endTime'])

        video_start = seconds_to_string(video_start)
        video_end = seconds_to_string(video_end)

        translated['video_start'] = video_start
        translated['video_end'] = video_end
        translated['game_start'] = game_start
        translated['game_end'] = game_end

        rtn.append(translated)
    return rtn
