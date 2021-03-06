import os
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
from lib.util.static_lol_data import get_champ_image, get_icon_image

POWER_HEADING = "Lane Dominance"


def _find_center(range_val, img_size):
    return int((range_val/2.0) - (img_size / 2.0))


def _assets_loc(file_name):
    return os.path.join(os.path.dirname(__file__), "assets", file_name)


def build_bar_tile(power_value, scale=100.0):
    marker = Image.open(_assets_loc("Square.png"))
    bar = Image.open(_assets_loc("PowerBar1.png"))

    img = Image.new('RGBA', (bar.width, marker.height))
    img.paste(bar, (0, img.height/4))

    power_pos = power_value + scale
    power_pos /= (2 * scale)
    power_pos *= bar.width

    img.paste(marker, (int(power_pos), 0), marker)
    return img


def build_champ_tile(champ, champ_lvl, level_side, version, pad=6):
    champ_img = get_champ_image(version, champ)

    new_im = Image.new('RGBA', (champ_img.width, champ_img.height))

    new_im.paste(champ_img, (0, 0))

    level_im = Image.new('RGBA', (champ_img.width/4, champ_img.height/4), color='black')

    font = ImageFont.truetype(_assets_loc("beaufortforlol-bold.otf"), 20)
    fill = "white"
    draw = ImageDraw.Draw(level_im)
    w, h = draw.textsize(str(champ_lvl), font=font)
    text_x = int((level_im.width - w) / 2)
    text_y = int((level_im.height - w) / 2)
    draw.text((text_x, 0), str(champ_lvl), fill=fill, font=font)

    if level_side == "left":
        x = 0
        y = new_im.height - level_im.height
        new_im.paste(level_im, (x, y))
    else:
        x = new_im.width - level_im.width
        y = new_im.height - level_im.height
        new_im.paste(level_im, (x, y))

    return new_im


def build_stat_tile(gold, cs, kills, deaths, assists, pad=4):
    score_icon = get_icon_image('5.5.1', 'score')
    minion_icon = get_icon_image('5.5.1', 'minion')

    score_icon_dem = (27, 50)
    minion_icon_dem = (30, 27)

    font = ImageFont.truetype(_assets_loc("compactalet.ttf"), 40)
    fill = "white"

    score_val = str(kills) + '/' + str(deaths) + '/' + str(assists)
    cs_val = str(cs)

    width = 260
    height = 50

    img = Image.new('RGBA', (width, height))
    icon_x = 0
    score = Image.open(_assets_loc("score_icon.png"))
    resize_size = 45
    score.thumbnail((resize_size, resize_size), resample=Image.LANCZOS)

    icon_y = int((height - score.height) / 2)
    img.paste(score, (0, icon_y))

    icon_x = int( (width/2.0) ) + 25
    icon_y = _find_center(height, minion_icon_dem[1]) - 2
    minion = Image.open(_assets_loc("minion.png"))
    resize_size = 50
    minion.thumbnail((resize_size, resize_size), resample=Image.LANCZOS)

    icon_y = int((height - minion.height) / 2) - 2
    img.paste(minion, (140, icon_y), minion)


    draw = ImageDraw.Draw(img)
    text_x = score_icon_dem[1] + pad
    text_y = _find_center(height, 24)
    draw.text((text_x, text_y), score_val, fill=fill, font=font)

    draw = ImageDraw.Draw(img)
    text_x = icon_x + minion_icon_dem[1] + pad + 10
    text_y = _find_center(height, 24)
    draw.text((text_x, text_y), cs_val, fill=fill, font=font)

    return img


def build_player_tile(champ_tile, stats_tile, stat_side, pad=10):
    champ_tile_width, champ_tile_height = champ_tile.size
    stats_tile_width, stats_tile_height = stats_tile.size

    total_width = champ_tile_width + pad + stats_tile_width
    total_height = max(champ_tile_height, stats_tile_height)

    new_im = Image.new('RGBA', (total_width, total_height))

    if stat_side == 'left':
        paste_x = 0
        paste_y = _find_center(total_height, stats_tile.height)
        new_im.paste(stats_tile, (paste_x, paste_y))

        paste_x = stats_tile_width + pad
        paste_y = int((total_height - champ_tile_height) / 2)
        new_im.paste(champ_tile, (paste_x, paste_y))
    else:
        paste_x = 0
        paste_y = int((total_height - champ_tile_height) / 2)
        new_im.paste(champ_tile, (paste_x, paste_y))

        paste_x = champ_tile_width + pad
        paste_y = _find_center(total_height, stats_tile.height)
        new_im.paste(stats_tile, (paste_x, paste_y))

    return new_im


def build_lane_tile(left_player, right_player, power_bar, pad=40):
    total_height = left_player.height
    total_width = left_player.width + pad + power_bar.width + pad + right_player.width

    new_im = Image.new('RGBA', (total_width, total_height))

    paste_x = 0
    paste_y = 0
    new_im.paste(left_player, (paste_x, paste_y))

    paste_x = left_player.width + pad
    paste_y = int(new_im.height / 2) - int(power_bar.height / 2)
    new_im.paste(power_bar, (paste_x, paste_y))

    paste_x = left_player.width + pad + power_bar.width + pad
    paste_y = 0
    new_im.paste(right_player, (paste_x, paste_y))

    return new_im


def build_lanes_tile(lanes_imgs, pad=10):
    total_width = max(map(lambda x: x.width, lanes_imgs))
    total_height = max(map(lambda x: x.height, lanes_imgs)) * 5 + pad * 4

    new_im = Image.new('RGBA', (total_width, total_height))
    y_pos = 0
    for champ_tile in lanes_imgs:
        new_im.paste(champ_tile, (0, y_pos))
        y_pos += champ_tile.height + pad

    return new_im


def build_heading_tile(team_1_gold, team_2_gold):
    font = ImageFont.truetype(_assets_loc("beaufortforlol-bold.otf"), 50)

    total_height = 50
    total_width = 950 + (40 * 2) + (120 * 2)

    heading_right = build_gold_heading(team_2_gold, "right")
    heading_left = build_gold_heading(team_1_gold, "left")

    new_im = Image.new('RGBA', (total_width, total_height))

    fill = "white"
    draw = ImageDraw.Draw(new_im)
    w, h = draw.textsize(POWER_HEADING, font=font)
    text_x = _find_center(new_im.width, w)
    text_y = -12
    draw.text((text_x, text_y), POWER_HEADING, fill=fill, font=font)

    new_im.paste(heading_left, (0, 0))
    new_im.paste(heading_right, (total_width - heading_right.width, 0))

    return new_im


def build_gold_heading(gold_value, icon_side, font=ImageFont.truetype(_assets_loc("beaufortforlol-bold.otf"), 40), pad=20):
    gold_value = str(round(gold_value / 1000.0, 1)) + "k"

    if icon_side == "left":
        team_fill = "royalblue"
    else:
        team_fill = "orangered"

    width = 180
    height = 50

    new_im = Image.new('RGBA', (width, height))

    draw = ImageDraw.Draw(new_im)

    w, h = draw.textsize(gold_value, fill=team_fill, font=font)

    if icon_side == "left":
        text_x = 0
    else:
        text_x = width - w

    text_y = -3
    draw.text((text_x, text_y), gold_value, fill=team_fill, font=font)

    icon = Image.open(_assets_loc("gold_icon.png"))
    resize_size = int(h*1.7)
    icon.thumbnail((resize_size, resize_size), resample=Image.LANCZOS)

    if icon_side == "left":
        icon_x = w
    else:
        icon_x = text_x - icon.width

    icon_y = int((height - icon.height) / 2)
    new_im.paste(icon, (icon_x, icon_y), icon)

    return new_im


def build_full_image(heading, lanes, pad=30):
    width = 1920
    height = heading.height + pad + lanes.height

    img = Image.new('RGBA', (width, height))

    lanes_x_center = _find_center(width, lanes.width)
    heading_x_center = _find_center(width, heading.width)

    img.paste(heading, (heading_x_center, 0))
    img.paste(lanes, (lanes_x_center, heading.height + pad))

    background = Image.open(_assets_loc("background1080.jpg"))
    img_y_pos = _find_center(background.height, img.height) - 20
    background.paste(img, (0, img_y_pos), img)
    return background


def build_sample():
    power = build_bar_tile(10)
    champ = build_champ_tile("Janna", 16, 'right', "6.15.1")
    stat = build_stat_tile(66666, 666, 66, 66, 66)
    player1 = build_player_tile(champ, stat, 'left')

    champ = build_champ_tile("Janna", 16, 'left', "6.15.1")
    stat = build_stat_tile(66666, 666, 66, 66, 66)
    player2 = build_player_tile(champ, stat, 'right')

    lane = build_lane_tile(player1, player2, power)

    lanes = build_lanes_tile([lane, lane, lane, lane, lane])
    heading = build_heading_tile(66666, 66666)

    full = build_full_image(heading, lanes, pad=10)

    rtn = full
    return rtn


if __name__ == "__main__":
    sample = build_sample()
    sample.show()
    # sample.save("test.png")
