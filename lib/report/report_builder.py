from lib.zip.inmemory_zip import InMemoryZip
from lib.image_generator.image_build import build_info_graphics
from lib.report.sort_data import sort_data
from lib.util.static_vals import REPORTS_DIR
from lib.game_analysis.video_download_template import video_download_batch_file
import json
import os

TYPES_OF_DATA = ['time_line_events', 'time_line_infographic', 'event_translation', 'video_analysis']


def build_report_file(game_analysis, match, match_name=None, file_path=None):
    if file_path is None:
        match_id = match.get('id', '')
        if match_name:
            file_path = os.path.join(REPORTS_DIR, match_name + "_" + match_id + ".zip")
        else:
            file_path = os.path.join(REPORTS_DIR, match_id+".zip")

    if not game_analysis:
        return

    time_stamp = 0
    for game in game_analysis:
        stmp = game.get('time_stamp', 0)
        time_stamp = stmp if stmp >= time_stamp else time_stamp

    if os.path.isfile(file_path):
        file_time_stamp = os.path.getmtime(file_path)
        if file_time_stamp > time_stamp:
            return

    imz = InMemoryZip()

    had_data = False
    files = {'infographics': []}
    video_list = []
    for game in game_analysis:
        name = game['name']
        video_list.append({'game_name': name, 'youtube_url': 'youtube_url'})
        if not game or 'time_line_events' not in game or 'time_line_infographic' not in game:
            continue

        had_data = False
        time_line_infographic = None
        for type_val in TYPES_OF_DATA:
            if type_val in game:
                had_data = True
                data = game[type_val]
                data = sort_data(data, type_val)
                imz.append(name + "_" + type_val + ".json", json.dumps(data, indent=2))
                if type_val == 'time_line_infographic':
                    time_line_infographic = game[type_val]

        if time_line_infographic:
            images = build_info_graphics(time_line_infographic)
            for i in range(len(images)):
                file_name = name + "_" + images[i].info.get('file_name', "infographic_" + str(i))
                imz.append_image(file_name, images[i])
                files['infographics'].append(file_name)

    imz.append('files.json', json.dumps(files, indent=2))
    imz.append("match_video_download.bat", video_download_batch_file(video_list))
    imz.append("match_info.json", json.dumps(match, indent=2))

    if had_data:
        imz.write_to_file(file_path)
