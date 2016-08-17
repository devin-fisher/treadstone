import base64
from moviepy.editor import VideoFileClip
# from imageio import imsave, RETURN_BYTES
import sys
from PIL import Image, ImageEnhance
import numpy


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
    if show:
        Image.fromarray(image).show()
    if image is not None:
        image = _crop_image(image)
        return _prep_image(image, show=show)


if __name__ == "__main__":
    path = sys.argv[1]
