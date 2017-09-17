from lib.image_generator.build_tiles import *


SIDES = ["left", "right"]


def build_side_of_lane(data, side, player_num, version):
    c_tile = build_champ_tile(data[side]['championId'][player_num], data[side]['playerLevel'][player_num], SIDES[side],
                              version)
    s_tile = build_stat_tile(data[side]['playerGold'][player_num]
                             , data[side]['minionsKilled'][player_num]
                             , data[side]['playerKills'][player_num]
                             , data[side]['playerDeaths'][player_num]
                             , data[side]['playerAssists'][player_num])
    p_tile = build_player_tile(c_tile, s_tile, SIDES[side])
    return p_tile


def build_info_graphics(infographic_data):
    version = "7.1.1"
    rtn = []
    timestamp2 = 0
    for data in infographic_data:
        lanes = []
        for i in xrange(5):
            left = build_side_of_lane(data, 0, i, version)
            right = build_side_of_lane(data, 1, i, version)
            power_bar = build_bar_tile(data[0]['power'][i])
            lane_img = build_lane_tile(left, right, power_bar)
            lanes.append(lane_img)

        lanes_img = build_lanes_tile(lanes)
        left_team_gold = data[0]['teamGold']
        right_team_gold = data[1]['teamGold']
        timestamp = data[0]['timeStamp']
        timediff = timestamp - timestamp2

        heading_img = build_heading_tile(left_team_gold, right_team_gold, timestamp, timediff)
        full_img = build_full_image(heading_img, lanes_img)

        file_name = "infographic_" + str(timestamp)
        full_img.info['file_name'] = file_name
        rtn.append(full_img)
        timestamp2 = timestamp
    return rtn


if __name__ == "__main__":
    sample = build_sample()
    sample.show()
    sample.save('test.png', 'PNG')
    pass
