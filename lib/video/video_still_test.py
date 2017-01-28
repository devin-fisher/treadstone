from moviepy.editor import VideoFileClip
from video_still import get_still_with_video
from video_still_machine import find_time_still
from video_analysis import standard_analysis
import video_still_util
from video_still_test_samples import SAMPLE_ANALYSIS

import numbers


def compare_element(elm1, elm2):
    if isinstance(elm1, list):
        if not compare_list(elm1, elm2):
            return False
    if isinstance(elm1, dict):
        if not compare_dict(elm1, elm2):
            return False
    else:
        if isinstance(elm1, numbers.Number) and isinstance(elm2, numbers.Number):
            return abs(elm1-elm2) <= 1
        elif cmp(elm1, elm2):
            return False

    return True


def compare_list(list1, list2):
    if len(list1) != len(list2):
        return False

    for i in range(len(list1)):
        compare_element(list1[i], list2[i])

    return True


def compare_dict(dict1, dict2):
    for key, value in dict1.iteritems():
        if key not in dict2:
            return False
        else:
            compare_element(value, dict2[key])

    return True


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


def test_all_video_analysis():
    for video, analysis in SAMPLE_ANALYSIS.iteritems():
        print "Doing analysis for '%s'" % video
        test_video_analysis(video, analysis)


def test_video_analysis(video_path, analysis):
    cal_analysis = standard_analysis(video_path, analysis['game_length'], verbose=False)
    if compare_dict(cal_analysis, analysis):
        results = "Equal"
    else:
        print "Calculate Values: " + str(cal_analysis)
        print "Expected Values: " + str(analysis)
        results = "NOT Equal!!"
    print("Results for '%s' are %s" % (video_path, results))

if __name__ == "__main__":
    # test_still_open_video('/home/devin.fisher/Kingdoms/lol/fmqeavjSfTg.mp4', 1927, 540)
    # test_still_open_video('/home/devin.fisher/Kingdoms/lol/fmqeavjSfTg.mp4', 1987, 600)
    test_all_video_analysis()
    # print(standard_analysis('/tmp/lol/oxtlhJBAAOQ.mp4', 2458, verbose=True))
    # print(str(standard_analysis("/home/devin.fisher/Kingdoms/lol/3O7OJY3X0yM-HD.mp4", 2391, verbose=True)))
    # print compare_dict(SAMPLE_ANALYSIS["/home/devin.fisher/Kingdoms/lol/fmqeavjSfTg.mp4"], SAMPLE_ANALYSIS["/home/devin.fisher/Kingdoms/lol/fmqeavjSfTg.mp4"])