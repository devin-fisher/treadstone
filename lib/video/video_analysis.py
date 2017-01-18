from video_still import get_still_with_video
from video_still_machine import find_time_still, get_time, is_expected_time
from moviepy.editor import VideoFileClip
import video_still_util as util
import math

from operator import add, sub

IMAGE_SPLITS_COUNT = 10.0
IMAGE_SPLIT_TIME = .999 / IMAGE_SPLITS_COUNT

WALK_DOWN_CYCLE = [10.0, 5.0, 1.0]

MAX_ITERATIONS = 100


def _test_start(video, video_time, game_test_time=45):
    at_game_test_time = get_time(video, video_time+game_test_time, show=False)
    return at_game_test_time == game_test_time


def _find_sec_change(video, video_time, game_time):
    video_time_plus_split = video_time
    c = 0
    while True:
        c += 1
        if c > 100:
            raise Exception("Unable to break loop!")
        video_time_plus_split += IMAGE_SPLIT_TIME
        cur_game_time = get_time(video, video_time_plus_split)
        if cur_game_time is None:
            # print("_find_sec_change iterations: " + str(c))
            return None, None

        if cur_game_time > game_time:
            # print("_find_sec_change iterations: " + str(c))
            return video_time_plus_split + IMAGE_SPLIT_TIME, cur_game_time # add a little bit of time, we don't want to be right on the edge


def find_start_point(video, game_test_time=45, bump_rate=45):
    cur_video = video.duration*.55
    max_time = video.duration
    operator = sub

    c = 0
    while True:
        c += 1
        if c > 100:
            raise Exception("Unable to break loop!")

        if cur_video > max_time or cur_video <= 0:
            raise Exception("Unable to find start time")

        found_game_time = get_time(video, cur_video, show=False)
        if found_game_time is None:
            cur_video = operator(cur_video, bump_rate)
            continue

        found_video_time, found_game_time = _find_sec_change(video, cur_video, found_game_time)

        if found_video_time is None or found_game_time is None:
            cur_video = operator(cur_video, bump_rate)
            continue

        proposed_start_video_time = found_video_time - found_game_time
        game_at_proposed = get_time(video, proposed_start_video_time + game_test_time, show=False)

        if game_at_proposed is None:
            cur_video = operator(cur_video, bump_rate)
            continue
        elif game_at_proposed == game_test_time:
            # print("find_start_point iterations: " + str(c))
            return proposed_start_video_time
        else:
            cur_video -= (found_game_time/2)
            continue


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


def _get_past_break(video, video_time, last_game_time, length, step=5):  # We should handle if this reaches towards the end of the video
    break_start_video_time = video_time
    c = 0
    while True:
        c += 1
        if c > 100:
            raise Exception("Unable to break loop!")
        video_time += step
        new_game_time = get_time(video, video_time, show=False)
        if new_game_time:
            game_time_diff = new_game_time - last_game_time
            if 0 < game_time_diff < 12:
                # print("_get_past_break iterations: " + str(c))
                return video_time, new_game_time
            video_time_diff = video_time - break_start_video_time
            if -20 <= int(video_time_diff - game_time_diff) <= 30:
                # print("_get_past_break iterations: " + str(c))
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

    c = 0
    while True:
        c += 1
        if c > 100:
            raise Exception("Unable to break loop!")
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

    # print("find_time_shifts iterations: " + str(c))
    return rtn_shifts


def standard_analysis(video_path, game_length, verbose=False):
    rtn = {}
    rtn['game_length'] = game_length

    video_obj = VideoFileClip(video_path)
    start = find_start_point(video_obj)

    rtn['start'] = start

    shifts = find_time_shifts(video_obj, start, game_length, verbose=verbose)
    rtn['shifts'] = shifts

    if shifts:
        end = shifts[-1]['end_time'] + (game_length - shifts[-1]['end_game_time'])
    else:
        end = start + game_length
    rtn['end'] = end

    return rtn


def start_only_analysis(video_path, game_length, verbose=False):
    rtn = {}
    rtn['game_length'] = game_length

    video_obj = VideoFileClip(video_path)
    start = find_start_point(video_obj)

    rtn['start'] = start

    rtn['shifts'] = []

    return rtn


if __name__ == "__main__":
    path = '/tmp/lol/f393a06c-c0dd-48e2-aa2d-abaecae7646c.mp4'
    video_obj = VideoFileClip(path)
    # break_video_start, break_game_start = _walk_cycle(_walk_forward, video_obj, 788.0778, 154.0, 1626)
    # break_video_past_break, break_game_past_break = _get_past_break(video_obj, 2446.1723, 1446.0, 1910)
    # print util.seconds_to_string(break_video_past_break)
    # print util.seconds_to_string(break_game_past_break)
    # time = get_time(video_obj, 978.0778, show=True)

    _get_past_break(video_obj, 2250.3737, 1671.0, 1657, step=5)
    # get_time(video_obj, 1249.4624, show=True)
    # output = standard_analysis(path, 1626, verbose=True)
    # print(output)
    pass
