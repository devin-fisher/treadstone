import sys
from moviepy.editor import VideoFileClip
from video_still import get_still_with_video, extract_parts
from video_still_util import seconds_to_string
import video_still_util
from video_still_test import SAMPLE_ANALYSIS

from sklearn.cross_validation import train_test_split
from sklearn.metrics import classification_report
from nolearn.dbn import DBN

from sklearn.externals import joblib

import pickle

import numpy


CONTRAST = 2.5
IMAGE_FILTER_THRESHOLD = 180

SAMPLE_STILL_DIR = '../../_samples/still_data/'


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
                # print("%s of %s" % (str(i), str(length)))
                image_data = get_still_with_video(video_obj, start_time+i, show=False)
                expected_digits = video_still_util.convert_seconds_to_parts(start_game_time+i)
                num = 0
                for part in extract_parts(image_data):
                    if part is None or part.size is not 165:
                        continue
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


def capture_video_data(rtn, video_path, analysis, verify_check=False):
    if not (analysis.get('should_verify', True)) and verify_check:
        return

    print video_path
    cur_time = dict()
    cur_time['start_time'] = analysis['start'] + 60
    cur_time['start_game_time'] = 60
    for shift in analysis['shifts']:
        cur_time['length'] = int((shift['start_time'] - 1) - cur_time['start_time'])
        print("Video:%s -- Start Time: %s -- Start Game Time: %s -- Length: %s"
              % (video_path,
                 seconds_to_string(cur_time['start_time']),
                 seconds_to_string(cur_time['start_game_time']),
                 seconds_to_string(cur_time['length'])))
        capture_digit_data(video_path, rtn, check_times=analysis.get('should_verify', True), **cur_time)
        cur_time['start_time'] = shift['end_time'] + 1
        cur_time['start_game_time'] = shift['end_game_time'] + 1


def capture_data(data_set_path='../../_samples/still_data/still_training_data.pkl', verify_check=False):
    rtn = dict()
    rtn['target'] = []
    rtn['data'] = []

    for video_path, analysis in SAMPLE_ANALYSIS.iteritems():
        capture_video_data(rtn, video_path, analysis, verify_check)

    rtn['target'] = numpy.asarray(rtn['target'])
    rtn['data'] = numpy.stack(rtn['data'])

    with open(data_set_path, 'wb') as f:
        pickle.dump(rtn, f)


def train_model(data_set_path='/home/devin.fisher/Kingdoms/treadstone/_samples/still_data/still_training_data.pkl'):
    # data_set = None
    with open(data_set_path, 'rb') as f:
        data_set = pickle.load(f)

    # with open('/home/devin.fisher/Kingdoms/lol/still_training_data2.pkl', 'rb') as f:
    #     data_set = pickle.load(f)

    # (train_x, test_x, train_y, test_y) = train_test_split(data_set['data'], data_set['target'], test_size=0.1)

    train_x = data_set['data']
    test_x = data_set['data']
    train_y = data_set['target']
    test_y = data_set['target']

    dbn = DBN(
        [-1, 300, -1],
        learn_rates=0.3,
        learn_rate_decays=0.9,
        epochs=60,
        verbose=1)
    dbn.fit(train_x, train_y)

    joblib.dump(dbn, 'digit_model.pkl', compress=9)

    # dbn = joblib.load('digit_model.pkl')

    # compute the predictions for the test data and show a classification report
    preds = dbn.predict(test_x)
    print classification_report(test_y, preds)


def dedup(data_set_path='../../_samples/still_data/still_training_data.pkl'):
    with open('/home/devin.fisher/Kingdoms/treadstone/_samples/still_data/still_training_data.pkl', 'rb') as f:
        data_set = pickle.load(f)

    rtn = dict()
    dedup_data = []
    dedup_target = []
    has = set()
    data = data_set['data']
    target = data_set['target']
    for i in xrange(len(target)):
        row = tuple(data[i])
        if row not in has:
            has.add(row)
            dedup_target.append(target[i])
            dedup_data.append(data[i])

    rtn['target'] = numpy.asarray(dedup_target)
    rtn['data'] = numpy.stack(dedup_data)

    with open(data_set_path, 'wb') as f:
        pickle.dump(rtn, f)


if __name__ == "__main__":
    train_model()
    # capture_data()
    # dedup()
