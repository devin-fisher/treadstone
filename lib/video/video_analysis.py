from video_still import get_still_with_video
from video_still_machine import find_time_still
from moviepy.editor import VideoFileClip

IMAGE_SPLITS_COUNT = 10.0
IMAGE_SPLIT_TIME = .999 / IMAGE_SPLITS_COUNT


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
            if _test_start(video, rtn_start_video_time):
                return rtn_start_video_time
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

        second_change_video_time = _find_sec_change(video, cur, found_game_time)

        if second_change_video_time is None:
            cur += bump_rate
            continue
        else:
            return second_change_video_time

if __name__ == "__main__":
    path = "/home/devin.fisher/Kingdoms/lol/79i_t9CCqDQ.mp4"
    video_obj = VideoFileClip(path)
    print find_start_point(video_obj)

    # time = 1401
    # game_time = 14
    # for i in xrange(100):
    #     image = get_still_with_video(video_obj, time)
    #     found_game_time = find_time_still(image)
    #     match = game_time == found_game_time
    #     print "t: %s expected: %s found: %s match: %s" % (str(time), str(game_time), str(found_game_time), str(match))
    #
    #     time += 1
    #     game_time += 1


