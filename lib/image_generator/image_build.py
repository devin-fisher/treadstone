import os
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
from PIL import ImageFile
from image_cache import get_item_image, get_summoner_image, get_champ_image, get_icon_image

from lib.video.video_still_util import seconds_to_string


def build_item_tile(items, version, pad=6, image_size=64):
    items = _get_item_images(items, version)
    _validate_item_images(items)

    place_triket = False

    total_width = image_size * 3 + pad * 3
    if place_triket:
        total_width += image_size
    max_height = image_size * 2 + pad

    # print(total_width)
    # print(max_height)

    new_im = Image.new('RGBA', (total_width, max_height))

    # Top Row
    x_offset = 0
    y_offset = 0
    for pos in range(3):
        im = items[pos]
        if im:
            new_im.paste(im, (x_offset, y_offset))
        x_offset += image_size + pad

    if place_triket:
        # Trinket
        im = items[3]
        hoz_center = int((max_height - image_size) / 2)
        if im:
            new_im.paste(im, (total_width - image_size, hoz_center))

    # Bottem Row
    x_offset = 0
    y_offset = image_size + pad

    for pos in range(4, 7):
        im = items[pos]
        if im:
            new_im.paste(im, (x_offset, y_offset))
        x_offset += image_size + pad

    return new_im


def build_champ_tile(champ, summoner1, summoner2, version, pad=6):
    champ_img = get_champ_image(version, champ)
    summoner1_img = get_summoner_image(version, summoner1)
    summoner2_img = get_summoner_image(version, summoner2)

    champ_img_width, champ_img_height = champ_img.size
    summoner1_img_width, summoner1_img_height = summoner1_img.size
    summoner2_img_width, summoner2_img_height = summoner2_img.size

    total_width = champ_img_width + pad + max(summoner1_img_width, summoner2_img_width)
    total_height = max(champ_img_height, (summoner1_img_height + pad + summoner2_img_height))

    # print(total_width)
    # print(total_height)

    new_im = Image.new('RGBA', (total_width, total_height))

    place_x = int((total_height - champ_img_height) / 2)
    new_im.paste(champ_img, (0, place_x))
    new_im.paste(summoner1_img, (champ_img_width + pad, 0))
    new_im.paste(summoner2_img, (champ_img_width + pad, summoner1_img_height + pad))

    return new_im


def build_player_tile(champ_tile, stats_tile, item_tile, pad=10):
    champ_tile_width, champ_tile_height = champ_tile.size
    stats_tile_width, stats_tile_height = stats_tile.size
    item_tile_width, item_tile_height = item_tile.size

    total_width = champ_tile_width + pad + stats_tile_width + pad + item_tile_width
    total_height = max(champ_tile_height, stats_tile_height, item_tile_height)

    # print(total_width)
    # print(total_height)

    new_im = Image.new('RGBA', (total_width, total_height))

    paste_x = 0
    paste_y = int((total_height - champ_tile_height) / 2)
    new_im.paste(champ_tile, (paste_x, paste_y))

    paste_x = champ_tile_width + pad
    paste_y = 0
    new_im.paste(stats_tile, (paste_x, paste_y))

    paste_x = champ_tile_width + pad + stats_tile_width + pad
    paste_y = 0
    new_im.paste(item_tile, (paste_x, paste_y))

    return new_im


def build_team_tile(champ_tiles, total_gold, pad=10):
    total_width = max(map(lambda x: x.width, champ_tiles))
    total_height = max(map(lambda x: x.height, champ_tiles)) * 5 + pad * 4

    # print(total_width)
    # print(total_height)

    new_im = Image.new('RGBA', (total_width, total_height))
    y_pos = 0
    for champ_tile in champ_tiles:
        new_im.paste(champ_tile, (0, y_pos))
        y_pos += champ_tile.height + pad

    return new_im


def build_stat_tile(gold, cs, kills, deaths, assists, pad=4):
    gold_icon = get_icon_image('5.5.1', 'gold')
    score_icon = get_icon_image('5.5.1', 'score')
    minion_icon = get_icon_image('5.5.1', 'minion')

    gold_icon_dem = (22, 18)
    score_icon_dem = (18, 19)
    minion_icon_dem = (22, 20)

    font = ImageFont.truetype(_assets_loc("compactalet.ttf"), 20)
    fill = "white"

    gold_val = str(round(gold / 1000.0, 1)) + "k"
    score_val = str(kills) + '/' + str(deaths) + '/' + str(assists)
    cs_val = str(cs)

    width = 55
    height = 134

    # print(width)
    # print(height)

    img = Image.new('RGBA', (width, height))

    draw = ImageDraw.Draw(img)
    icon_x = int((width / 2) - (gold_icon_dem[0] / 2))
    icon_y = pad
    img.paste(gold_icon, (icon_x, icon_y))

    w, h = draw.textsize(gold_val, font=font)
    text_x = int((width - w) / 2)
    text_y = int(icon_y + gold_icon_dem[1] + (pad / 2))
    draw.text((text_x, text_y), gold_val, fill=fill, font=font)

    draw = ImageDraw.Draw(img)
    icon_x = int((width / 2) - (score_icon_dem[0] / 2))
    icon_y = text_y + h + (pad * 2)
    img.paste(score_icon, (icon_x, icon_y))

    w, h = draw.textsize(score_val, font=font)
    text_x = int((width - w) / 2)
    text_y = int(icon_y + gold_icon_dem[1] + (pad / 2))
    draw.text((text_x, text_y), score_val, fill=fill, font=font)

    if cs:
        draw = ImageDraw.Draw(img)
        icon_x = int((width / 2) - (minion_icon_dem[0] / 2))
        icon_y = text_y + h + (pad * 2)
        img.paste(minion_icon, (icon_x, icon_y))

        w, h = draw.textsize(cs_val, font=font)
        text_x = int((width - w) / 2)
        text_y = int(icon_y + gold_icon_dem[1] + (pad / 2))
        draw.text((text_x, text_y), cs_val, fill=fill, font=font)

    return img


def build_score_tile(team_1_kills, team_2_kills, team_1_gold, team_2_gold, pad=20):
    width = 600
    height = 720

    font = ImageFont.truetype(_assets_loc("beaufortforlol-bold.otf"), 35)
    team_1_fill = "royalblue"
    team_2_fill = "orangered"

    # print(width)
    # print(height)

    img = Image.new('RGBA', (width, height))

    team_1_gold = str(round(team_1_gold / 1000.0, 1)) + "k"
    team_2_gold = str(round(team_2_gold / 1000.0, 1)) + "k"

    draw = ImageDraw.Draw(img)

    v_pad = pad*3
    max_y = 0

    w, h = draw.textsize(str(team_1_kills), font=font)
    text_x = int(width / 2 - w - v_pad)
    text_y = pad
    draw.text((text_x, text_y), str(team_1_kills), fill=team_1_fill, font=font)
    max_y = max(max_y, text_y+h)

    w, h = draw.textsize(str(team_2_kills), font=font)
    text_x = int(width / 2 + v_pad)
    draw.text((text_x, text_y), str(team_2_kills), fill=team_2_fill, font=font)
    max_y = max(max_y, text_y + h)

    icon = Image.open(_assets_loc("score_icon.png"))
    resize_size = int(h*1.7)
    icon.thumbnail((resize_size, resize_size), resample=Image.LANCZOS)
    icon_x = int(width/2 - (icon.width/2))
    icon_y = int((text_y+h/2) - icon.height/2)
    img.paste(icon, (icon_x, icon_y))

    text_y += 4*pad+h

    w, h = draw.textsize(team_1_gold, font=font)
    text_x = int(width / 2 - w - v_pad)
    draw.text((text_x, text_y), team_1_gold, fill=team_1_fill, font=font)
    max_y = max(max_y, text_y + h)

    w, h = draw.textsize(team_2_gold, font=font)
    text_x = int(width / 2 + v_pad)
    draw.text((text_x, text_y), team_2_gold, fill=team_2_fill, font=font)
    max_y = max(max_y, text_y + h)

    icon = Image.open(_assets_loc("gold_icon.png"))
    resize_size = int(h*1.7)
    icon.thumbnail((resize_size, resize_size), resample=Image.LANCZOS)
    icon_x = int(width/2 - (icon.width/2))
    icon_y = int((text_y+h/2) - icon.height/2)
    img.paste(icon, (icon_x, icon_y))

    max_y += pad

    img = img.crop((0,0, img.width, max_y))

    return img


def build_full_image(team_1_tile, team_2_tile, score_tile, side_pad=40):
    width = 1280
    height = 720

    img = Image.new('RGBA', (width, height))

    team_1_tile.thumbnail((550, 550), Image.ANTIALIAS)
    team_2_tile.thumbnail((550, 550), Image.ANTIALIAS)

    paste_x = int(width / 2 - (score_tile.width / 2))
    paste_y = int(height / 2 - (score_tile.height / 2))
    img.paste(score_tile, (paste_x, paste_y))

    paste_x = side_pad
    paste_y = int((height - team_1_tile.height) / 2)
    img.paste(team_1_tile, (paste_x, paste_y))

    paste_x = width - team_2_tile.width - side_pad
    paste_y = int((height - team_2_tile.height) / 2)
    img.paste(team_2_tile, (paste_x, paste_y))

    background = Image.open(_assets_loc("background2.jpg"))
    background.paste(img, (0, 0), img)
    return background


def _assets_loc(file):
    return os.path.join(os.path.dirname(__file__), "assets", file)


def _find_width_stat_tile(gold_str, score_str, font):
    img = Image.new('RGBA', (500, 500))
    draw = ImageDraw.Draw(img)
    return max((draw.textsize(gold_str, font=font)[0] + 8), (draw.textsize(score_str, font=font)[0] + 8))


def _get_item_images(items, version):
    rtn = []
    for item in items:
        if item:
            rtn.append(get_item_image(version, item))
        else:
            rtn.append(None)

    if len(rtn) < 7:
        for i in range(len(rtn), 7):
            rtn.append(None)
    return rtn


def _validate_item_images(items):
    if len(items) is not 7:
        # print("List don't include 7 items")
        pass

    for im in items:
        if not isinstance(im, ImageFile.ImageFile) and im is not None:
            # print("Not all items or None")
            pass

    sizes = []
    for im in items:
        if im:
            if im.size[0] is not im.size[1]:
                # print("Not all items are square")
                pass
            sizes.append(im.size[0])

    if len(set(sizes)) > 1:
        # print("Not all items are same size")
        pass


def build_info_graphics(infographic_data):
    version = "6.15.1"
    rtn = []
    for data in infographic_data:
        timestamp = 0
        team_tiles = []
        team_kills = []
        team_gold = []
        for team_data in data:
            timestamp = team_data['timeStamp']
            team_kills.append(team_data.get('teamKills', 0))
            team_gold.append(team_data.get('teamGold', 0))
            team_player_tiles = []
            for player_num in xrange(len(team_data['playerItem'])):
                i_tile = build_item_tile(team_data['playerItem'][player_num], version)

                c_tile = build_champ_tile(team_data['championId'][player_num]
                                          , team_data['summonerSpell'][player_num][0]
                                          , team_data['summonerSpell'][player_num][1]
                                          , version)

                s_tile = build_stat_tile(team_data['playerGold'][player_num]
                                             , team_data['minionsKilled'][player_num]
                                             , team_data['playerKills'][player_num]
                                             , team_data['playerDeaths'][player_num]
                                             , team_data['playerAssists'][player_num])

                p_tile = build_player_tile(c_tile, s_tile, i_tile)
                team_player_tiles.append(p_tile)

            team_tiles.append(build_team_tile(team_player_tiles, 0))

        s_tile = build_score_tile(team_kills[0]
                                      , team_kills[1]
                                      , team_gold[0]
                                      , team_gold[1])
        img = build_full_image(team_tiles[0], team_tiles[1], s_tile)
        img.info['file_name'] = "infographic_" + seconds_to_string(timestamp).replace(':', '-')
        rtn.append(img)
    return rtn


def build_sample_image():
    items_list = [get_item_image("6.15.1", "3073"), get_item_image("6.15.1", "3071"), get_item_image("6.15.1", "1001"),
                  get_item_image("6.15.1", "3340"), get_item_image("6.15.1", "1401"), None, None]
    items_list = ["3073", "3071", "1001", "3340", "1401", None, None]
    item_tile = build_item_tile(items_list, "6.15.1")

    stats_tile = build_stat_tile(66666, 666, 66, 66, 66)

    champ_tile = build_champ_tile("Janna", "SummonerFlash", "SummonerFlash", "6.15.1")
    champ_tile2 = build_champ_tile("Akali", "SummonerFlash", "SummonerFlash", "6.15.1")
    champ_tile3 = build_champ_tile("Ashe", "SummonerFlash", "SummonerFlash", "6.15.1")
    champ_tile4 = build_champ_tile("Elise", "SummonerFlash", "SummonerFlash", "6.15.1")
    champ_tile5 = build_champ_tile("Shen", "SummonerFlash", "SummonerFlash", "6.15.1")

    player_tile = build_player_tile(champ_tile, stats_tile, item_tile)
    player_tile2 = build_player_tile(champ_tile2, stats_tile, item_tile)
    player_tile3 = build_player_tile(champ_tile3, stats_tile, item_tile)
    player_tile4 = build_player_tile(champ_tile4, stats_tile, item_tile)
    player_tile5 = build_player_tile(champ_tile5, stats_tile, item_tile)

    team_tile = build_team_tile([player_tile, player_tile2, player_tile3, player_tile4, player_tile5], 0)

    score_tile = build_score_tile(66, 66, 666666, 666666)

    full_tile = build_full_image(team_tile, team_tile.copy(), score_tile)

    return full_tile

if __name__ == "__main__":
    sample = build_sample_image()
    sample.show()
    # sample.save('test.png', 'PNG')
