import sys
import os
from video_still_lookup_table import get_still_hash_table, lookup_still_hash_image
from video_still import get_still
from video_still_hash import video_still_hash_small, video_still_hash_large, _prep_image
from PIL import Image


def hash_compare(video_path, ht, time, game_time, cal_game_time):
    out_dir = "/tmp/hash_compare/"
    # os.makedirs(out_dir)

    contrast = 200000

    a = get_still(path, time)
    print "actual:"
    print video_still_hash_small(a)
    print video_still_hash_large(a)
    _prep_image(a, contrast_val=contrast).save(out_dir+'a.png')

    b = Image.open('/tmp/stills/'+str(game_time)+'.png')
    print "expected:"
    print video_still_hash_small(b)
    print video_still_hash_large(b)
    _prep_image(b, contrast_val=contrast).save(out_dir + 'b.png')

    if cal_game_time:
        c = Image.open('/tmp/stills/'+str(cal_game_time)+'.png')
        print "calculate:"
        print video_still_hash_small(c)
        print video_still_hash_large(c)
        _prep_image(c, contrast_val=contrast).save(out_dir + 'c.png')


def test_hash(path, time, ht, expected_time):
    image = get_still(path, time)
    found_game_time = lookup_still_hash_image(ht, image)

    match = expected_time == found_game_time

    if match is False or True:
        print "time: %s expected: %s found: %s match: %s" % (str(time), str(game_time), str(found_game_time), str(match))

    if match is False:
        hash_compare(path, ht, time, expected_time, found_game_time)
        raw_input("Continue:")

    return match, found_game_time


if __name__ == "__main__":
    path = sys.argv[1]
    ht = get_still_hash_table()
    time = 1777
    game_time = 129
    # image = get_still(path, time)

    # hash_compare(path, ht, 1826, 178)

    # time = 1826 # 178
    # image = get_still(path, time)
    # image.show()
    # found_game_time = lookup_still_hash_image(ht, image)
    # print found_game_time

    # video_still_hash_large(image)

    match, found_game_time = test_hash(path, 1803, ht, 155)

    # for i in xrange(100):
    #     match, found_game_time = test_hash(path, time, ht, game_time)
    #
    #     time += 1
    #     game_time += 1

