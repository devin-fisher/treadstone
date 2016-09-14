from video_still import get_still_with_video
from video_still_machine import find_time_still, get_time, is_expected_time
from moviepy.editor import VideoFileClip
import video_still_util as util
import math

from operator import add, sub

IMAGE_SPLITS_COUNT = 10.0
IMAGE_SPLIT_TIME = .999 / IMAGE_SPLITS_COUNT

# WALK_DOWN_CYCLE = [240.0, 60.0, 20.0, 5.0, 1.0]
WALK_DOWN_CYCLE = [10.0, 5.0, 1.0]


def _test_start(video, video_time, game_test_time=45):
    at_game_test_time = get_time(video, video_time+game_test_time, show=False)
    return at_game_test_time == game_test_time


def _find_sec_change(video, video_time, game_time, game_test_time=45):
    video_time_plus_split = video_time
    while True:
        video_time_plus_split += IMAGE_SPLIT_TIME
        cur_game_time = get_time(video, video_time_plus_split)
        if cur_game_time is None:
            return None

        if cur_game_time > game_time:
            rtn_start_video_time = video_time_plus_split - cur_game_time
            if _test_start(video, rtn_start_video_time, game_test_time=game_test_time):
                return rtn_start_video_time + IMAGE_SPLIT_TIME # add a little bit of time, we don't want to be right on the edge
            else:
                return None


def find_start_point(video, game_test_time=45, bump_rate=10):
    cur = video.duration/2
    max_time = video.duration

    while True:
        if cur > max_time:
            return None

        found_game_time = get_time(video, cur, show=False)
        if found_game_time is None:
            cur += bump_rate
            continue

        second_change_video_time = _find_sec_change(video, cur, found_game_time, game_test_time=game_test_time)

        if second_change_video_time is None:
            cur += bump_rate
            continue
        else:
            return second_change_video_time


def _walk_op(video, video_time, game_time, length, step, operator):
    last_good_video_time = video_time
    last_good_game_time = game_time
    for i in xrange(1, int(math.ceil(length/step))):
        video_time = operator(video_time, step)
        game_time = operator(game_time, step)

        if is_expected_time(video, video_time, game_time):
            last_good_video_time = video_time
            last_good_game_time = game_time
        else:
            # print "At: %s Expected: %s Found: %s" % (video_time, util.seconds_to_string(game_time), util.seconds_to_string(found_game_time))
            return last_good_video_time, last_good_game_time

    return None, None


def _walk_backwards(video, video_time, game_time, length, step):
    return _walk_op(video, video_time, game_time, length, step, sub)


def _walk_forward(video, video_time, game_time, length, step):
    return _walk_op(video, video_time, game_time, length, step, add)


def _walk_cycle(func, video, video_time, game_time, length):
    good_video_time = video_time
    good_game_time = game_time
    for step in WALK_DOWN_CYCLE:
        good_video_time, good_game_time = func(video, good_video_time, good_game_time, length, step)

        if good_video_time is None:
            return good_video_time, good_game_time

    if length - good_game_time <= 25:  # very near the end
        return None, None
    return good_video_time, good_game_time


def _get_past_break(video, video_time, last_game_time, length, step=5):
    while True:
        video_time += step
        new_game_time = get_time(video, video_time, show=False)
        if new_game_time:
            if -60 <= int(last_game_time - new_game_time) <= 60:
                return video_time, new_game_time

#TODO Must detect errors - backwards time shifts
def find_time_shifts(video, start_video_time, length, verbose=False, inital_game_time_shift=61):
    if verbose:
        print "Game Start: " + util.seconds_to_string(start_video_time) + " -- " + str(start_video_time) + "\n"

    start_video_time += inital_game_time_shift
    cur_video_time = start_video_time
    expected_game_time = inital_game_time_shift

    rtn_shifts = []
    had_errors = False

    while True:
        break_video_start, break_game_start = _walk_cycle(_walk_forward, video, cur_video_time, expected_game_time, length)

        if break_video_start is None:
            end = cur_video_time + (length - expected_game_time)

            if verbose:
                print "Game End: " + util.seconds_to_string(end)

            break

        if verbose:
            print "Break Start: " + str((util.seconds_to_string(break_video_start), util.seconds_to_string(break_game_start)))

        break_video_past_break, break_game_past_break = _get_past_break(video, break_video_start, break_game_start, length)

        break_video_end, break_game_end = _walk_cycle(_walk_backwards, video, break_video_past_break, break_game_past_break, length)

        if break_video_end < break_video_start or break_game_end < break_game_start:
            had_errors = True
            cur_video_time = break_video_past_break
            expected_game_time = break_game_past_break
            continue

        if verbose:
            print "Break End: " + str((util.seconds_to_string(break_video_end), util.seconds_to_string(break_game_end)))
            print ""

        did_shift = (break_video_end - break_video_start) != (break_game_end - break_game_start)
        rtn_shifts.append({'start_time': break_video_start, 'start_game_time': break_game_start, 'end_time': break_video_end, 'end_game_time': break_game_end, 'did_shift': did_shift})
        cur_video_time = break_video_end
        expected_game_time = break_game_end

    if verbose:
        print str(rtn_shifts)

    return rtn_shifts

def standard_analysis(video_path, game_length, verbose=False):
    rtn = {}
    rtn['game_length'] = game_length

    video_obj = VideoFileClip(video_path)
    start = find_start_point(video_obj)

    rtn['start'] = start

    shifts = find_time_shifts(video_obj, start, game_length, verbose=verbose)
    rtn['shifts'] = shifts

    end = shifts[-1]['end_time'] + (game_length - shifts[-1]['end_game_time'])
    rtn['end'] = end

    return rtn


if __name__ == "__main__":
    path = "/home/devin.fisher/Kingdoms/lol/xbjnWx7YCyg.mp4"
    # break_video_start, break_game_start = _walk_cycle(_walk_forward, VideoFileClip(path), 2763.7094, 991.0, 2381)
    # print str((break_video_start, break_game_start ))
    # print "Break Start"
    # print (util.seconds_to_string(break_video_start),
    #        util.seconds_to_string(break_game_start))
    print(standard_analysis(path, 1880, verbose=True))

