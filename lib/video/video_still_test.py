from moviepy.editor import VideoFileClip
from video_still import get_still_with_video
from video_still_machine import find_time_still
from video_still_util import convert_min_sec_to_sec
from video_analysis import standard_analysis
import video_still_util

import numbers

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

SAMPLE_ANALYSIS = {
    "/home/devin.fisher/Kingdoms/lol/79i_t9CCqDQ.mp4":
    {
        'start': 651.3048,
        'end': 2240.3048,
        'game_length': 1594,
        'shifts':
            [
                {'start_game_time': 611.0,
                 'start_time': 1262.3048,
                 'did_shift': False,
                 'end_time': 1282.3048,
                 'end_game_time': 631},
                {'start_game_time': 1457.0,
                 'start_time': 2108.3048,
                 'did_shift': True,
                 'end_time': 2163.3048,
                 'end_game_time': 1517}
            ]
    }
    ,
    "/home/devin.fisher/Kingdoms/lol/fmqeavjSfTg.mp4":
    {
        'start': 1386.8696000000002,
        'end': 3674.8696,
        'game_length': 2292,
        'shifts':
            [
                {'start_game_time': 1048.0,
                 'start_time': 2434.8696,
                 'did_shift': True,
                 'end_time': 2479.8696,
                 'end_game_time': 1097
                 }
                ,
                {'start_game_time': 1641.0,
                 'start_time': 3023.8696,
                 'did_shift': False,
                 'end_time': 3075.8696,
                 'end_game_time': 1695.0
                 }
                ,
                {'start_game_time': 1930.0,
                 'start_time': 3312.8696,
                 'did_shift': False,
                 'end_time': 3330.8696,
                 'end_game_time': 1948.0}
            ]
    }
    ,
    "/home/devin.fisher/Kingdoms/lol/pFgEnbRlv00.mp4":
        {
            'start': 1264.9040999999995,
            'end': 3400.9040999999997,
            'game_length': 2141,
            'shifts': [{
                'start_game_time': 219.0,
                'start_time': 1483.9040999999995,
                'did_shift': False,
                'end_time': 1496.9040999999995,
                'end_game_time': 232.0
            }, {
                'start_game_time': 585.0,
                'start_time': 1849.9040999999995,
                'did_shift': False,
                'end_time': 1866.9040999999995,
                'end_game_time': 602.0
            }, {
                'start_game_time': 710.0,
                'start_time': 1974.9040999999995,
                'did_shift': False,
                'end_time': 1998.9040999999995,
                'end_game_time': 734.0
            }, {
                'start_game_time': 880.0,
                'start_time': 2144.9040999999997,
                'did_shift': True,
                'end_time': 2158.9040999999997,
                'end_game_time': 899.0
            }, {
                'start_game_time': 1599.0,
                'start_time': 2858.9040999999997,
                'did_shift': False,
                'end_time': 2888.9040999999997,
                'end_game_time': 1629
            }, {
                'start_game_time': 1964.0,
                'start_time': 3223.9040999999997,
                'did_shift': False,
                'end_time': 3265.9040999999997,
                'end_game_time': 2006.0
            }]
        }
    ,
    "/home/devin.fisher/Kingdoms/lol/UpS-erY7L3k.mp4":
        {
            'start': 1777.7094000000009,
            'end': 4153.709400000001,
            'game_length': 2381,
            'shifts': [{
                'start_game_time': 341.0,
                'start_time': 2118.7094000000006,
                'did_shift': False,
                'end_time': 2129.7094000000006,
                'end_game_time': 352.0
            }, {
                'start_game_time': 531.0,
                'start_time': 2308.7094000000006,
                'did_shift': False,
                'end_time': 2329.7094000000006,
                'end_game_time': 552.0
            }, {
                'start_game_time': 726.0,
                'start_time': 2503.7094000000006,
                'did_shift': False,
                'end_time': 2517.7094000000006,
                'end_game_time': 740.0
            }, {
                'start_game_time': 963.0,
                'start_time': 2740.7094000000006,
                'did_shift': True,
                'end_time': 2763.7094000000006,
                'end_game_time': 991.0
            }, {
                'start_game_time': 1671.0,
                'start_time': 3443.7094000000006,
                'did_shift': False,
                'end_time': 3471.7094000000006,
                'end_game_time': 1699.0
            }, {
                'start_game_time': 2091.0,
                'start_time': 3863.7094000000006,
                'did_shift': False,
                'end_time': 3893.7094000000006,
                'end_game_time': 2121
            }, {
                'start_game_time': 2222.0,
                'start_time': 3994.7094000000006,
                'did_shift': False,
                'end_time': 4029.7094000000006,
                'end_game_time': 2257
            }]
        }
    ,
    "/home/devin.fisher/Kingdoms/lol/pCAKGLPRimY.mp4" :
        {
            'start': 1004.2291999999997,
            'end': 2910.2291999999998,
            'game_length': 1910,
            'shifts': [{
                'start_game_time': 1071.0,
                'start_time': 2075.2291999999998,
                'did_shift': True,
                'end_time': 2116.2291999999998,
                'end_game_time': 1116.0
            }, {
                'start_game_time': 1446.0,
                'start_time': 2446.2291999999998,
                'did_shift': False,
                'end_time': 2475.2291999999998,
                'end_game_time': 1475.0
            }, {
                'start_game_time': 1550.0,
                'start_time': 2550.2291999999998,
                'did_shift': False,
                'end_time': 2574.2291999999998,
                'end_game_time': 1574.0
            }, {
                'start_game_time': 1747.0,
                'start_time': 2747.2291999999998,
                'did_shift': False,
                'end_time': 2773.2291999999998,
                'end_game_time': 1773.0
            }]
        }
    ,
    "/home/devin.fisher/Kingdoms/lol/xbjnWx7YCyg.mp4":
        {
            'start': 422.3838999999994,
            'end': 2298.3838999999994,
            'game_length': 1880,
            'shifts': [{
                'start_game_time': 359.0,
                'start_time': 781.3838999999994,
                'did_shift': False,
                'end_time': 794.3838999999994,
                'end_game_time': 372.0
            }, {
                'start_game_time': 715.0,
                'start_time': 1137.3838999999994,
                'did_shift': False,
                'end_time': 1167.3838999999994,
                'end_game_time': 745
            }, {
                'start_game_time': 1607.0,
                'start_time': 2029.3838999999994,
                'did_shift': True,
                'end_time': 2030.3838999999994,
                'end_game_time': 1612.0
            }, {
                'start_game_time': 1702.0,
                'start_time': 2120.3838999999994,
                'did_shift': False,
                'end_time': 2137.3838999999994,
                'end_game_time': 1719.0
            }]
        }
}


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
    cal_analysis = standard_analysis(video_path, analysis['game_length'])
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
    # print compare_dict(SAMPLE_ANALYSIS["/home/devin.fisher/Kingdoms/lol/fmqeavjSfTg.mp4"], SAMPLE_ANALYSIS["/home/devin.fisher/Kingdoms/lol/fmqeavjSfTg.mp4"])