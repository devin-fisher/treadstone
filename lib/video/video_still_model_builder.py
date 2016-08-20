import sys
from moviepy.editor import VideoFileClip
from video_still import get_still_with_video, extract_parts
from video_still_util import convert_min_sec_to_sec
import video_still_util

from sklearn.cross_validation import train_test_split
from sklearn.metrics import classification_report
from nolearn.dbn import DBN

from sklearn.externals import joblib

import pickle

import numpy

# from video_still_machine import extract_parts


CONTRAST = 2.5
IMAGE_FILTER_THRESHOLD = 180

SAMPLE_STILL_DIR = '../../_samples/still_data/'

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


def get_conformation(question):
    # raw_input returns the empty string for "enter"
    yes = set(['yes', 'y', 'ye', ''])
    no = set(['no', 'n'])

    print(question+"[y/n] ")
    choice = raw_input().lower()
    if choice in yes:
        return True
    elif choice in no:
        return False
    else:
        sys.stdout.write("Please respond with 'yes' or 'no'")


def check_time(video_obj, time, expected_game_time, should_check):
    if should_check:
        print "End Expect %s:" % video_still_util.convert_parts_to_string(video_still_util.convert_seconds_to_parts(expected_game_time))
        get_still_with_video(video_obj, time, show=True)
        return get_conformation('Was as expected:')
    else:
        return True


def capture_digit_data(path, data, interval_sec=1, check_times=False, **kwargs):
    video_obj = VideoFileClip(path)
    start_time = kwargs.get('start_time')
    length = kwargs.get('length')
    start_game_time = kwargs.get('start_game_time')
    new_data = dict()
    new_data['target'] = []
    new_data['data'] = []

    if check_time(video_obj, start_time, start_game_time, check_times):
        for i in xrange(length):
            if not check_times:
                image_data = get_still_with_video(video_obj, start_time+i)
                expected_digits = video_still_util.convert_seconds_to_parts(start_game_time+i)
                num = 0
                for part in extract_parts(image_data):
                    new_data['target'].append(int(expected_digits[num]))
                    new_data['data'].append(part)
                    num += interval_sec

        if check_time(video_obj, start_time+i, start_game_time+i, check_times):
            data['target'].extend(new_data['target'])
            data['data'].extend(new_data['data'])
        else:
            print "Fix %s -- %s" % (str(path), str(kwargs))

    else:
        print "Fix %s -- %s" % (str(path), str(kwargs))


def train_model(data_set_path='/home/devin.fisher/Kingdoms/treadstone/_samples/still_data/still_training_data.pkl'):
    data_set = None
    with open(data_set_path, 'rb') as f:
        data_set = pickle.load(f)

    (train_x, test_x, train_y, test_y) = train_test_split(data_set['data'], data_set['target'], test_size=0.33)

    dbn = DBN(
        [-1, 300, -1],
        learn_rates=0.3,
        learn_rate_decays=0.9,
        epochs=10,
        verbose=1)
    dbn.fit(train_x, train_y)

    joblib.dump(dbn, 'digit_model.pkl', compress=9)

    # compute the predictions for the test data and show a classification report
    preds = dbn.predict(test_x)
    print classification_report(test_y, preds)

if __name__ == "__main__":
    train_model()
    # rtn = dict()
    # rtn['target'] = []
    # rtn['data'] = []
    #
    # for video_path, times in SAMPLE_RANGES.iteritems():
    #     capture_digit_data(video_path, rtn, check_times=False, **times)
    #
    # rtn['target'] = numpy.asarray(rtn['target'])
    # rtn['data'] = numpy.asarray(rtn['data'])
    #
    # with open('../../_samples/still_data/still_training_data.pkl', 'wb') as f:
    #     pickle.dump(rtn, f)
