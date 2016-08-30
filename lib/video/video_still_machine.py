import numpy
from video_still import get_still, extract_parts
import video_still_util

from sklearn.externals import joblib

IMAGE_FILTER_THRESHOLD = 180

MODEL = joblib.load('digit_model.pkl')


def find_time_still(image_data):
    parts_image = extract_parts(image_data)

    digits = []
    for part in parts_image:
        digit = MODEL.predict(numpy.atleast_2d(part))
        # print "Predicted digit" + str(digit)
        digits.append(int(digit))

    return video_still_util.convert_parts_to_seconds(digits)


if __name__ == "__main__":
    im = get_still("/home/devin.fisher/Kingdoms/lol/79i_t9CCqDQ.mp4", 1278, show=True)
    print find_time_still(im)
