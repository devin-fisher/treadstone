import sys
import os
from moviepy.editor import VideoFileClip
from video_still import get_still_with_video

from sklearn.cross_validation import train_test_split
from sklearn.metrics import classification_report
from nolearn.dbn import DBN

from PIL import Image

from sklearn.externals import joblib
import numpy

import pickle

CONTRAST = 2.5
IMAGE_FILTER_THRESHOLD = 180

SAMPLE_STILL_DIR = '../../_samples/still_data/'

# TODO these are broken.

def capture_still_data():
    rtn = dict()
    rtn['target'] = []
    rtn['data'] = []

    for t in xrange(10):
        for i in os.listdir(os.path.join(SAMPLE_STILL_DIR, "stills")):
            if i.endswith(".png"):

                num = 0
                file_path = os.path.join(SAMPLE_STILL_DIR, "stills", i)
                file_num = i.split('.')[0]
                expected_digits = convert_seconds_to_parts(file_num)
                for part in extract_parts(numpy.array(Image.open(file_path))):
                    rtn['target'].append(int(expected_digits[num]))
                    rtn['data'].append(part)
                    num += 1

    rtn['target'] = numpy.array(rtn['target'])
    rtn['data'] = numpy.array(rtn['data'])

    with open('../../_samples/still_data/still_training_data.pkl', 'wb') as f:
        pickle.dump(rtn, f)

def train_model(data_set_path='/home/devin.fisher/Kingdoms/treadstone/lol_img_gen/still_data/still_training_data.pkl'):
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

    # dbn = joblib.load('digit_model.pkl')

    # compute the predictions for the test data and show a classification report
    preds = dbn.predict(test_x)
    print classification_report(test_y, preds)

def get_still_every_n(path, start_time, end_time, game_start_time, interval_sec=1):
    cur_time = start_time
    game_time = game_start_time
    video = VideoFileClip(path)
    while cur_time <= end_time:
        still_data = get_still_with_video(video, cur_time)

        game_time += 1
        cur_time += interval_sec


if __name__ == "__main__":
    path = sys.argv[1]
    game_time = 14
    offset = 0
    start = 1401 + offset
    # end = 5650.6944
    get_still_every_n(path, start, start+60, game_start_time=game_time)
