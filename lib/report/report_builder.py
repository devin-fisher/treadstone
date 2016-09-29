from lib.zip.inmemory_zip import InMemoryZip
from lib.image_generator.image_build import build_info_graphics
import json
import os

TYPES_OF_DATA = ['time_line_events', 'time_line_infographic', 'event_translation', 'video_analysis']


def build_report_file(game_analysis, match_id, file_path):
    if not game_analysis:
        return

    imz = InMemoryZip()
    had_data = False
    for game in game_analysis:
        name = game['name']
        if not game or 'time_line_events' not in game or 'time_line_infographic' not in game:
            continue

        had_data = False
        time_line_infographic = None
        for type_val in TYPES_OF_DATA:
            if type_val in game:
                had_data = True
                imz.append(name + "_" + type_val + ".json", json.dumps(game[type_val], indent=2))
                if type_val == 'time_line_infographic':
                    time_line_infographic = game[type_val]

        if time_line_infographic:
            images = build_info_graphics(time_line_infographic)
            for i in range(len(images)):
                imz.append_image(name + "_" + images[i].info.get('file_name', "infographic_" + str(i)), images[i])

    if had_data:
        if not os.path.isfile(file_path):
            imz.write_to_file(file_path)
