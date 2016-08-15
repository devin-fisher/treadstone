import sys
import os
import pickle
import editdistance
from PIL import Image
from moviepy.editor import VideoFileClip
from video_still import get_still_with_video
from video_still_hash import video_still_hash_small_file, video_still_hash_large_file
from video_still_hash import video_still_hash_small, video_still_hash_large


def get_still_every_n(path, start_time, end_time, interval_sec=1, game_start_time=0, save_dir=None):
    cur_time = start_time
    rtn = []
    game_time = game_start_time
    while cur_time <= end_time:
        print game_time
        video = VideoFileClip(path)
        still_data = get_still_with_video(video, cur_time)
        if save_dir:
            still_data.save(save_dir + str(game_time)+".png")
            # with open(save_dir + str(game_time)+".png", 'wb') as f:
            #     f.write(still_data)
        game_time += 1
        cur_time += interval_sec


def build_still_hash_table(dir_path, pickle_loc="/tmp/time_lookup_ht.pickle"):
    rtn = {}
    for i in os.listdir(dir_path):
        if i.endswith(".png"):
            hash_small_val = video_still_hash_small_file(os.path.join(dir_path, i))
            hash_large_val = video_still_hash_large_file(os.path.join(dir_path, i))
            sub_ht = rtn.get(hash_small_val, {})
            time = i.split(".")[0]
            sub_ht[hash_large_val] = time
            rtn[hash_small_val] = sub_ht

    print len(rtn)
    if pickle_loc:
        with open(pickle_loc, 'wb') as f:
            pickle.dump(rtn, f)


def get_still_hash_table(pickle_loc="/tmp/time_lookup_ht.pickle"):
    with open(pickle_loc, 'rb') as f:
        return pickle.load(f)


def lookup_still_hash_file(hash_table, path):
    return lookup_still_hash_image(hash_table, Image.open(path))


def lookup_still_hash_image(hash_table, image):
    small_hash = video_still_hash_small(image)
    large_hash = video_still_hash_large(image)
    cur_time = None
    cur_min = sys.maxsize
    if small_hash in hash_table:
        for key, val in hash_table[small_hash].iteritems():
            distance = editdistance.eval(key, large_hash)
            if distance < cur_min:
                cur_min = distance
                cur_time = val

        return int(cur_time)

    else:
        return None

if __name__ == "__main__":
    path = sys.argv[1]
    game_time = 1707
    offset = 1702
    start = 1647.6944 + offset
    end = 5650.6944
    # stills = get_still_every_n(path, start, start+360, game_start_time=game_time, save_dir="/tmp/stills/")
    build_still_hash_table("/tmp/stills/")
