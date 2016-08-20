from moviepy.editor import VideoFileClip
import sys
from PIL import Image, ImageEnhance
import numpy
import cv2


IMAGE_SPLITS_COUNT = 10.0
IMAGE_SPLIT_TIME = .999 / IMAGE_SPLITS_COUNT

CONTRAST = 2.5
IMAGE_FILTER_THRESHOLD = 180


def _prep_image(image, show=False, contrast_val=CONTRAST, image_filter_threshold=IMAGE_FILTER_THRESHOLD):
    image = Image.fromarray(image)
    image = image.convert('LA')
    contrast = ImageEnhance.Contrast(image)
    image = contrast.enhance(contrast_val)
    image = image.convert('L')
    image = numpy.array(image)
    image = _convert_binary_array(image, image_filter_threshold)
    if show:
        Image.fromarray(image).show()
    return image


def _convert_binary_array(numpy_array, threshold=IMAGE_FILTER_THRESHOLD):
    for i in range(len(numpy_array)):
        for j in range(len(numpy_array[0])):
            if numpy_array[i][j] > threshold:
                numpy_array[i][j] = 255
            else:
                numpy_array[i][j] = 0
    return numpy_array


def _crop_image(image):
    if (720, 1280, 3) == image.shape:
        return image[55:68, 625:653]
    raise Exception("Video Resolution has changed")


def get_still(path_val, pos_sec, show=False):
    video = VideoFileClip(path_val)
    return get_still_with_video(video, pos_sec, show=show)


def get_still_with_video(video, pos_sec, show=False):
    image = video.get_frame(pos_sec)
    # if show:
    #     Image.fromarray(image).show()
    if image is not None:
        image = _crop_image(image)
        return _prep_image(image, show=show)


def _normalize_part(image, width=6, height=9, show=False):
    image = image.copy().reshape(image.shape[0] * image.shape[1])
    image = image.copy()
    image.resize(width*height, refcheck=False)

    if show:
        cv2.imshow("", image.reshape((height, width)))
        cv2.waitKey()

    return image / 255.0


def extract_part(contour, full_image, show=False):
    x, y, w, h = cv2.boundingRect(contour)
    part = full_image[y:y + h, x:x + w]
    if show:
        cv2.imshow("", part)
        cv2.waitKey()
    part = _normalize_part(part)

    return part


def extract_parts(image_data):
    contours, hierarchy = cv2.findContours(image_data.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    def contours_cmp(a, b):
        return cv2.boundingRect(a)[0].__cmp__(cv2.boundingRect(b)[0])

    def filter_colon_dots(contour):
        return cv2.boundingRect(contour)[3] >= 4

    contours = sorted(contours, cmp=contours_cmp)
    contours = filter(filter_colon_dots, contours)

    for c in contours:
        yield extract_part(c, image_data)

if __name__ == "__main__":
    path = sys.argv[1]
