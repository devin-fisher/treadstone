import sys
from PIL import Image
from image_cache import get_item_image, get_summoner_image, get_champ_image
import PIL

def build_item_tile(items, version, pad = 6, image_size = 64):
    items = _get_item_images(items, version)
    _validate_item_images(items)

    # image_size = 64

    total_width = image_size*4 + pad*3
    max_height = image_size * 2 + pad

    print total_width
    print max_height

    new_im = Image.new('RGBA', (total_width, max_height))

    #Top Row
    x_offset = 0
    y_offset = 0
    for pos in xrange(3):
        im = items[pos]
        if im:
            new_im.paste(im, (x_offset,y_offset))
        x_offset += image_size + pad

    #Trinket
    im = items[3]
    hoz_center = (max_height-image_size)/2
    if im:
        new_im.paste(im, (total_width-image_size, hoz_center))

    #Bottem Row
    x_offset = 0
    y_offset = image_size + pad

    for pos in xrange(4,7):
        im = items[pos]
        if im:
            new_im.paste(im, (x_offset,y_offset))
        x_offset += image_size + pad

    return new_im

def build_champ_tile(champ, summoner1, summoner2, version, pad = 6):
    champ_img = get_champ_image(version, champ)
    summoner1_img = get_summoner_image(version, summoner1)
    summoner2_img = get_summoner_image(version, summoner2)

    champ_img_width, champ_img_height  = champ_img.size
    summoner1_img_width, summoner1_img_height  = summoner1_img.size
    summoner2_img_width, summoner2_img_height  = summoner2_img.size

    total_width = champ_img_width + pad + max(summoner1_img_width, summoner2_img_width)
    total_hight = max(champ_img_height, (summoner1_img_height + pad + summoner2_img_height))

    print total_width
    print total_hight

    new_im = Image.new('RGBA', (total_width, total_hight))

    new_im.paste(champ_img, (0,(total_hight-champ_img_height)/2))
    new_im.paste(summoner1_img, (champ_img_width+pad, 0))
    new_im.paste(summoner2_img, (champ_img_width+pad, summoner1_img_height + pad))

    return new_im

def build_player_tile(champ_tile, item_tile, pad = 20):
    champ_tile_width, champ_tile_height  = champ_tile.size
    item_tile_width, item_tile_height  = item_tile.size

    total_width = champ_tile_width + pad + item_tile_width
    total_hight = max(champ_tile_height, item_tile_height)

    print total_width
    print total_hight

    new_im = Image.new('RGBA', (total_width, total_hight))

    new_im.paste(champ_tile, (0,(total_hight-champ_tile_height)/2))
    new_im.paste(item_tile, (champ_tile_width+pad, 0))

    return new_im


def _get_item_images(items, version):
    rtn = []
    for item in items:
        if item:
            rtn.append(get_item_image(version, item))
        else:
            rtn.append(None)
    return rtn

def _validate_item_images(items):
    if len(items) is not 7:
        print("List don't include 7 items")
        #return

    for im in items:
        if not isinstance(im, PIL.ImageFile.ImageFile) and im is not None:
            print("Not all items or None")

    sizes = []
    for im in items:
        if im:
            if im.size[0] is not im.size[1]:
                print("Not all items are square")
            sizes.append(im.size[0])

    if len(set(sizes)) > 1:
        print "Not all items are same size"


if __name__ == "__main__":
    items = [get_item_image("6.15.1", "3073"), get_item_image("6.15.1", "3071"), get_item_image("6.15.1", "1001"), get_item_image("6.15.1", "3340"), get_item_image("6.15.1", "1401"), None, None]
    items = ["3073", "3071", "1001", "3340", "1401", None, None]
    item_tile = build_item_tile(items, "6.15.1")
    champ_tile = build_champ_tile("Janna", "SummonerFlash", "SummonerFlash", "6.15.1")

    player_tile = build_player_tile(champ_tile, item_tile)
    player_tile.show()
    # player_tile.save('test.png', 'PNG')
