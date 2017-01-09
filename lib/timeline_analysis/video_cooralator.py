from collections import OrderedDict
from lib.video.video_still_util import seconds_to_string


def _convert_millisec_to_sec(mil):
    if mil > 6000:
        return mil/1000
    else:
        return mil


def _closer_with_shift(video_break, time, shift=.5, max_distance= 5):
    start_delta = abs(video_break['start_game_time'] - time)
    end_delta = abs(video_break['end_game_time'] - time)
    if start_delta is end_delta:
        raise Exception("Event Boundary is equal distance of break")
    elif start_delta < end_delta:
        if start_delta >= max_distance:
            raise Exception("Event Boundary is more than Max Distance from break boundary")
        else:
            return video_break['start_game_time'] - shift, video_break['start_time'] - shift
    else:  # end_delta is less than start_delta
        if end_delta >= max_distance:
            raise Exception("Event Boundary is more than Max Distance from break boundary")
        else:
            return video_break['end_game_time'] + shift, video_break['end_time'] + shift


def _find_video_time(video_breaks, game_time):
    cur_shift_video = video_breaks['start']
    cur_shift_game = 0
    game_time = _convert_millisec_to_sec(game_time)
    for video_break in video_breaks['shifts']:
        if game_time <= video_break['start_game_time']:
            rtn = cur_shift_video + (game_time - cur_shift_game)
            return game_time, rtn
        elif game_time <= video_break['end_game_time']:  # if the time is during the break
            mod_game_time, mod_video_time = _closer_with_shift(video_break, game_time)
            return mod_game_time, mod_video_time
        else:
            cur_shift_video = video_break['end_time']
            cur_shift_game = video_break['end_game_time']

    return game_time, cur_shift_video + (game_time - cur_shift_game)


def video_event_translator(events, video_breaks):
    rtn = []
    for range_data in events:
        translated = OrderedDict()

        game_start, video_start = _find_video_time(video_breaks, range_data['startTime'])
        game_end, video_end = _find_video_time(video_breaks, range_data['endTime'])

        translated['video_start'] = video_start
        translated['video_end'] = video_end
        translated['game_start'] = game_start
        translated['game_end'] = game_end

        rtn.append(translated)
    return rtn
