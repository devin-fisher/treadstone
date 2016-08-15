import base64
from moviepy.editor import VideoFileClip
# from imageio import imsave, RETURN_BYTES
import sys
from PIL import Image

IMAGE_SPLITS_COUNT = 10.0
IMAGE_SPLIT_TIME = .999 / IMAGE_SPLITS_COUNT

IMAGE_FORMAT = "png"


def find_mid_sec(video):
    return video.duration/2


def get_mid_stills(path):
    video = VideoFileClip(path)
    mid_sec = find_mid_sec(video)
    mid_sec = mid_sec
    print mid_sec
    rtn = []
    for i in xrange(int(IMAGE_SPLITS_COUNT)):
        cur_time = mid_sec + (i * IMAGE_SPLIT_TIME)
        rtn.append((cur_time,get_still_with_video(video, cur_time)))

    return rtn


def get_still(path, pos_sec):
    video = VideoFileClip(path)
    return get_still_with_video(video, pos_sec)


def get_still_with_video(video, pos_sec):
    image = video.get_frame(pos_sec)
    if image is not None:
        image = image[55:68, 625:653]
        return Image.fromarray(image)
        # cv2.imshow("still",image)
        # cv2.waitKey()
        # buf = imsave(RETURN_BYTES, image, format="."+IMAGE_FORMAT)
        # return buf

# def wrap_url_data_schema(data):
#     return "data:image/"+IMAGE_FORMAT+";base64," + base64.b64encode(data)

if __name__ == "__main__":
    path = sys.argv[1]
    # still_data_list = get_mid_stills(path)
    # with open("/tmp/still.html", 'w') as f:
    #     for image in still_data_list:
    #         f.write('<div>')
    #         f.write(str(image[0]))
    #         f.write('<img src="'+wrap_url_data_schema(image[1])+'" />')
    #         f.write('</div>')
