import lib.video.video_still_util as util
from collections import OrderedDict


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
        start = _find_video_time(video_breaks, range_data['startTime'])
        end = _find_video_time(video_breaks, range_data['endTime'])
        print str((util.seconds_to_string(start), util.seconds_to_string(end)))
        translated['startTime'] = start
        translated['endTime'] = end
        rtn.append(translated)
    return rtn
