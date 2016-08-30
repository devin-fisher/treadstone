from video_still import get_still_with_video
from video_still_machine import find_time_still
from moviepy.editor import VideoFileClip
import video_still_util
import math

from operator import add, sub

IMAGE_SPLITS_COUNT = 10.0
IMAGE_SPLIT_TIME = .999 / IMAGE_SPLITS_COUNT

# WALK_DOWN_CYCLE = [240.0, 60.0, 20.0, 5.0, 1.0]
WALK_DOWN_CYCLE = [10.0, 5.0, 1.0]


def get_time(video, video_time, show=False):
    image_data = get_still_with_video(video, video_time, show)
    game_time = find_time_still(image_data)
    return game_time


def _test_start(video, video_time, game_test_time=30):
    at_game_test_time = get_time(video, video_time+game_test_time)
    return at_game_test_time == game_test_time


def _find_sec_change(video, video_time, game_time, game_test_time=30):
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


def find_start_point(video, game_test_time=30, bump_rate=10):
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

        found_game_time = get_time(video, video_time, show=False)

        if game_time == found_game_time:
            last_good_video_time = video_time
            last_good_game_time = game_time
        else:
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

        # print (video_still_util.seconds_to_string(good_video_time),
        #        video_still_util.seconds_to_string(good_game_time))

        if good_video_time is None:
            return good_video_time, good_game_time

    if length - good_game_time <= 20:  # very near the end
        return None, None
    return good_video_time, good_game_time


def _get_past_break(video, video_time, last_game_time, length, step=5):
    while True:
        video_time += step
        new_game_time = get_time(video, video_time, show=False)
        if new_game_time:
            return video_time, new_game_time


def find_time_shifts(video, start_video_time, length):
    start_video_time += 61
    cur_video_time = start_video_time
    expected_game_time = 61

    rtn_shifts = []

    while True:
        break_video_start, break_game_start = _walk_cycle(_walk_forward, video, cur_video_time, expected_game_time, length)

        if break_video_start is None:
            end = cur_video_time + (length - expected_game_time)
            print "Game End"
            print video_still_util.seconds_to_string(end)
            break

        print "Break Start"
        print (video_still_util.seconds_to_string(break_video_start),
               video_still_util.seconds_to_string(break_game_start))

        break_video_end, break_game_end = _get_past_break(video, break_video_start, break_game_start, length)

        break_video_end, break_game_end = _walk_cycle(_walk_backwards, video, break_video_end, break_game_end, length)

        print "Break End"
        print (video_still_util.seconds_to_string(break_video_end),
               video_still_util.seconds_to_string(break_game_end))

        did_shift = (break_video_end - break_video_start) != (break_game_end - break_game_start)
        rtn_shifts.append({'start_time': break_video_start, 'start_game_time': break_game_start, 'end_time': break_video_end, 'end_game_time': break_game_end, 'did_shift': did_shift})
        cur_video_time = break_video_end
        expected_game_time = break_game_end

    return rtn_shifts

def standard_analysis(video_path, game_length, verbose=False):
    rtn = {}
    rtn['game_length'] = game_length

    video_obj = VideoFileClip(video_path)
    start = find_start_point(video_obj)

    rtn['start'] = start

    if verbose:
        print "Game Start: " + video_still_util.seconds_to_string(start)

    shifts = find_time_shifts(video_obj, start, game_length)
    rtn['shifts'] = shifts

    if verbose:
        for shift in shifts:
            print "Break Start: " + str((video_still_util.seconds_to_string(shift['start_time']),
                   video_still_util.seconds_to_string(shift['start_game_time'])))

            print "Break End: " + str((video_still_util.seconds_to_string(shift['end_time']),
                   video_still_util.seconds_to_string(shift['end_game_time'])))

            print "Did Shift: " + str(shift['did_shift'])


    end = shifts[-1]['end_time'] + (game_length - shifts[-1]['end_game_time'])
    rtn['end'] = end
    if verbose:
        print "Game End: " + video_still_util.seconds_to_string(end)

    return rtn


if __name__ == "__main__":
    path = "/home/devin.fisher/Kingdoms/lol/fmqeavjSfTg.mp4"
    print(standard_analysis(path, 2292, verbose=True))
    # video_obj = VideoFileClip(path)
    # # start = find_start_point(video_obj)
    # # print "start:" + str(start)
    # start = 651.3048
    # length_val = 1594
    #
    # print "start:" + str(start)
    #
    # print find_time_shifts(video_obj, start, length_val)

