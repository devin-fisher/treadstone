from moviepy.editor import VideoFileClip
from video_still import get_still_with_video
from video_still_machine import find_time_still
from video_still_util import convert_min_sec_to_sec
import video_still_util

SAMPLE_RANGES = {
    "/home/devin.fisher/Kingdoms/lol/79i_t9CCqDQ.mp4":
        {'start_time': 1970, 'length': 100, 'start_game_time': 1318}
    ,
    "/home/devin.fisher/Kingdoms/lol/fmqeavjSfTg.mp4":
        {'start_time': convert_min_sec_to_sec("23:22"),
         'length': convert_min_sec_to_sec("40:32") - convert_min_sec_to_sec("23:22"),
         'start_game_time': convert_min_sec_to_sec("0:15")}
    ,
    "/home/devin.fisher/Kingdoms/lol/pFgEnbRlv00.mp4":
        {'start_time': convert_min_sec_to_sec("33:19"),
         'length': convert_min_sec_to_sec("35:31") - convert_min_sec_to_sec("33:19"),
         'start_game_time': convert_min_sec_to_sec("12:14")}
    ,
    "/home/devin.fisher/Kingdoms/lol/pFgEnbRlv00.mp4":
        {'start_time': convert_min_sec_to_sec("36:00"),
         'length': convert_min_sec_to_sec("47:29") - convert_min_sec_to_sec("36:00"),
         'start_game_time': convert_min_sec_to_sec("15:00")}
    ,
    "/home/devin.fisher/Kingdoms/lol/pFgEnbRlv00.mp4":
        {'start_time': convert_min_sec_to_sec("48:10"),
         'length': convert_min_sec_to_sec("53:29") - convert_min_sec_to_sec("48:10"),
         'start_game_time': convert_min_sec_to_sec("27:10")}
    ,
    "/home/devin.fisher/Kingdoms/lol/pFgEnbRlv00.mp4":
        {'start_time': convert_min_sec_to_sec("54:27"),
         'length': convert_min_sec_to_sec("56:38") - convert_min_sec_to_sec("54:27"),
         'start_game_time': convert_min_sec_to_sec("33:27")}
}


def test_still_open_video(path, time, game_time):
    video_obj = VideoFileClip(path)
    return test_still(video_obj, path, time, game_time)


def test_still(video_obj, path, time, game_time):
    image = get_still_with_video(video_obj, time, show=False)
    found_game_time = find_time_still(image)
    match = game_time == found_game_time
    if match is False:
        print "t: %s expected: %s found: %s match: %s -- %s" % \
              (str(video_still_util.seconds_to_string(time)), str(video_still_util.seconds_to_string(game_time)),
               str(video_still_util.seconds_to_string(found_game_time)), str(match), path)


def test_video_range(path, **kwargs):
    video_obj = VideoFileClip(path)
    start_time = kwargs.get('start_time')
    length = kwargs.get('length')
    start_game_time = kwargs.get('start_game_time')
    for i in xrange(length):
        test_still(video_obj, path, start_time + i, start_game_time + i)


if __name__ == "__main__":
    test_still_open_video('/home/devin.fisher/Kingdoms/lol/fmqeavjSfTg.mp4', 1927, 540)
    test_still_open_video('/home/devin.fisher/Kingdoms/lol/fmqeavjSfTg.mp4', 1987, 600)
    # for video_path, times in SAMPLE_RANGES.iteritems():
    #     test_video_range(video_path, **times)