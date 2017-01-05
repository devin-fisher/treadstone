import os
import numpy
from video_still import get_still, extract_parts, get_still_with_video
import video_still_util

from sklearn.externals import joblib

IMAGE_FILTER_THRESHOLD = 180

MODEL = joblib.load(os.path.join(os.path.dirname(__file__), 'digit_model.pkl'))

COMMON_ERROR_DIGITS = {4: 9}


def get_time(video, video_time, show=False):
    image_data = get_still_with_video(video, video_time, show)
    game_time = find_time_still(image_data)
    return game_time


def _is_hard_expected_time(video, video_time, expected_game_time, show=False):
    return get_time(video, video_time, show=show) == expected_game_time


def _check_common_errors(game_time, expected_game_time):
    if game_time is None:
        return False

    game_time_parts = video_still_util.convert_seconds_to_parts(game_time)
    expected_game_time_parts = video_still_util.convert_seconds_to_parts(expected_game_time)

    if len(game_time_parts) != len(expected_game_time_parts):
        return False

    error_count = 0
    for i in range(len(game_time_parts)):
        if game_time_parts[i] != expected_game_time_parts[i]:
            if COMMON_ERROR_DIGITS.get(game_time_parts[i]) == expected_game_time_parts[i]:
                error_count += 1
            else:
                return False

    return error_count == 1


def is_expected_time(video, video_time, expected_game_time, show=False):
    game_time = get_time(video, video_time, show=show)
    if game_time == expected_game_time:
        return True
    else:
        if _is_hard_expected_time(video, video_time + .2, expected_game_time, show=show):
            return True
        if _is_hard_expected_time(video, video_time - .2, expected_game_time, show=show):
            return True
        return _check_common_errors(game_time, expected_game_time)


def find_time_still(image_data):
    parts_image = extract_parts(image_data)

    digits = []
    try:
        for part in parts_image:
            if part is None:
                return None
            digit = MODEL.predict(numpy.atleast_2d(part))
            digits.append(int(digit))
    except ValueError:
        return None

    return video_still_util.convert_parts_to_seconds(digits)


if __name__ == "__main__":
    im = get_still("/home/devin.fisher/Kingdoms/lol/UpS-erY7L3k.mp4", 2923.7094-.5, show=True)
    print video_still_util.seconds_to_string(find_time_still(im))
