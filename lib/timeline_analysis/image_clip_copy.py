
from moviepy.editor import ImageClip
from moviepy.editor import VideoFileClip
from moviepy.editor import concatenate_videoclips
from moviepy.editor import CompositeVideoClip
from moviepy.editor import AudioFileClip
from moviepy.video.fx import fadein
from moviepy.video.fx import fadeout
import requests
import json
from tkinter.filedialog import askopenfilename
import subprocess

def get_file_path():
    filename = askopenfilename()
    path = filename[0:filename.rfind("/")+1]
    path = path.replace('/','\\')
    return path

def get_game_number():
    game_number = 2
    return game_number



def get_report_info(path):
     file_path = path + "files.json"
     with open(file_path) as json_data:
        report_info = json.load(json_data)
     return report_info

def get_number_games(report_info):
    number_games = 0
    for a in range(1,6):
        check = True
        for b in range(0, len(report_info['infographics'])):
            infographic = report_info['infographics'][b]
            if (infographic[1:2] == str(a) and check == True):
                number_games = number_games + 1
                check = False


    return number_games

def get_event_translation(path, game_number):
    translation_path = path + 'G' + str(game_number) + '_event_translation.json'
    with open(translation_path) as json_data:
            event_translation = json.load(json_data)
    return event_translation

def create_image_video(path, report_info):

    infographic_list = []
    counter = 0
    for b in range(0, len(report_info['infographics'])):
        infographic = report_info['infographics'][b]
        audio = AudioFileClip("E:\Youtube\EU_Spring_2017\Week1\MSFvsGIA\silence.wav")
        clip = ImageClip(path + report_info['infographics'][b] + ".png",duration=3).set_audio(audio).fadein(1)
        clip.write_videofile(path + report_info['infographics'][b] + ".ts",fps=60, codec='libx264',
             audio_codec='aac',
             temp_audiofile='temp-audio.m4a',
             remove_temp=True)
        counter = counter + 1
        infographic_list.append(counter)


def create_sub_clips(path, game_number, event_translation):
    for a in range(0, len(event_translation)):
        duration = event_translation[a]['video_end'] - event_translation[a]['video_start']
        fade_end = duration - 3
        ss = event_translation[a]['video_start']
        ss_transition = event_translation[a]['video_start'] + 2
        input_vid = "G" + str(game_number) + "_full_game_video.mp4"
        vf = "fade=in:st=0:d=2,fade=out:st=13:d=2"
        video_start = int(ss)
        clip_name = str(game_number) + '-' + str(video_start)
        #
        subprocess.call(['ffmpeg', '-y', '-ss', str(ss), '-i', path + input_vid, '-t', str(duration), '-vf', 'fade=in:st=0:d=2,fade=out:st=' + str(fade_end) + ':d=2', '-af', 'afade=t=in:ss=0:d=3,afade=t=out:st=' + str(fade_end) + ':d=2',  '-preset',  'ultrafast',  '-avoid_negative_ts', 'make_zero', '-fflags', '+genpts', path + clip_name + '.ts'])




def make_ts_copies(path, game_number, report_info, event_translation, ts_copies):
    time_before = 0
    ts_copies.append('Game' + str(game_number))
    for a in range(0, len(event_translation)):
        start_time = event_translation[a]['video_start']
        game_time = event_translation[a]['game_end']
        for b in range(0, len(report_info['infographics'])):
            infographic = report_info['infographics'][b]
            if (int(infographic[1:2]) == game_number):
                print(int(infographic[1:2]))
                time = int(infographic[15:])
                print(start_time)
                print(time)
                print('------')
                if (time < game_time and time > time_before):
                    # subprocess.call(['ffmpeg', '-n', '-i', path + infographic + '.mp4', '-c', 'copy', path + infographic + '.ts'])
                    ts_copies.append(infographic)

        clip_name = str(game_number) + '-' + str(int(start_time))
        # subprocess.call(['ffmpeg', '-n', '-i', path + clip_name + '.mp4', '-c', 'copy', path + clip_name + '.ts'])
        # subprocess.call(['ffmpeg', '-n', '-i', path + clip_name + '_in.mp4', '-c', 'copy', path + clip_name + '_in.ts'])
        # subprocess.call(['ffmpeg', '-n', '-i', path + clip_name + '_out.mp4', '-c', 'copy', path + clip_name + '_out.ts'])
        # ts_copies.append(clip_name+'_in')
        ts_copies.append(clip_name)
        # ts_copies.append(clip_name+'_out')

        time_before = game_time
    print(ts_copies)
    return ts_copies

def make_concat_txt_file(path, ts_copies):
    for a in range(0, len(ts_copies)):
         if(a == 0):
             subprocess.call(['echo', 'file', "'" + ts_copies[a] + '.ts' + "'", '>', 'concat.txt'])
         else:
             subprocess.call(['echo', 'file', "'" + ts_copies[a] + '.ts' + "'", '>>', 'concat.txt'])



def concatinate(path, game_number, ts_copies):
    concat_list = 'E:\Youtube\Video\Intro_Final.ts|'
    for a in range(0, len(ts_copies)):
        if (a == len(ts_copies)-1):
            concat_list = concat_list + path + ts_copies[a]+ '.ts'
        elif (ts_copies[a][1:2] == 'a'):
            concat_list = concat_list + 'E:\Youtube\Video\\' + ts_copies[a] + '.ts' + '|'
        else:
            concat_list = concat_list + path + ts_copies[a]+ '.ts' + '|'
    print(concat_list)
    subprocess.call(['ffmpeg', '-f', 'mpegts', '-i', 'concat:' + concat_list, '-c', 'copy', '-bsf:a', 'aac_adtstoasc', path + 'match_highlights.mp4'])
    # print('ffmpeg -f mpegts -i "concat:clip1.ts|clip2.ts" -c copy -bsf:a aac_adtstoasc ' + path + 'match_highlights_test.mp4')

def make_transitions_video():
    for a in range(1,6):
        audio = AudioFileClip("E:\Youtube\EU_Spring_2017\Week1\MSFvsGIA\silence.wav")
        clip = ImageClip('E:\Youtube\Video\Game' + str(a) + '.png',duration=3).set_audio(audio)
        clip.write_videofile('E:\Youtube\Video\Game' + str(a) + '.mp4',fps=60, codec='libx264',
             audio_codec='aac',
             temp_audiofile='temp-audio.m4a',
             remove_temp=True)

def transition_ts_copy(path,number_games):
    video_path = 'E:\Youtube\Video\\'
    concat_all = []
    concat_all.append('E:\Youtube\Video\Intro_Final.ts')
    for a in range(1,number_games+1):
        transition = 'Game' + str(a) + '.ts'
        short = 'G' + str(a) + '_short'
        concat_all.append(video_path + transition)
        concat_all.append(path + short+'.ts')
        subprocess.call(['ffmpeg', '-n', '-i', path + short + '.mp4', '-c', 'copy', path + short +'.ts'])
    return(concat_all)

def concatenate_shorts(path,concat_all):
    concat_list = ''
    for a in range(0, len(concat_all)):
        if (a == len(concat_all)-1):
            concat_list = concat_list + concat_all[a]
        else:
            concat_list = concat_list + concat_all[a] + '|'
    print(concat_list)
    subprocess.call(['ffmpeg', '-f', 'mpegts', '-i', 'concat:' + concat_list, '-c', 'copy', '-bsf:a', 'aac_adtstoasc', path + 'match_highlights.ts'])

def clean_clips(path,ts_copies):
    for a in range(0,len(ts_copies)):
        subprocess.call(['del', path + ts_copies[a] + '.mp4'], shell=True)
        subprocess.call(['del', path + ts_copies[a] + '.ts'], shell=True)



def clean_shorts(path,number_games):
    for a in range(1, number_games+1):
        subprocess.call(['del', path + 'G' + str(a) + '_short.mp4'], shell=True)
        subprocess.call(['del', path + 'G' + str(a) + '_short.ts'], shell=True)

if __name__ == "__main__":

    ts_copies = []
    path = get_file_path()
    # game_number = get_game_number()
    report_info = get_report_info(path)
    number_games = get_number_games(report_info)
    # make_transitions_video()
    # transition_ts_copy()
    create_image_video(path, report_info)
    for a in range(1,number_games+1):
          game_number = a
          event_translation = get_event_translation(path,game_number)
          create_sub_clips(path, game_number, event_translation)
          ts_copies = make_ts_copies(path, game_number, report_info, event_translation,ts_copies)
    concatinate(path, game_number, ts_copies)
    clean_clips(path,ts_copies)
    # concat_all = transition_ts_copy(path,number_games)
    # concatenate_shorts(path,concat_all)y
    # clean_shorts(path, number_games)