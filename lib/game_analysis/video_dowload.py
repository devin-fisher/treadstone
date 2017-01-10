from __future__ import unicode_literals
import os
from urllib import ContentTooShortError as UrllibContentTooShortError
import youtube_dl
from youtube_dl.utils import ContentTooShortError as DLContentTooShortError
import time
from tempfile import gettempdir

MAX_RETIRES = 3
WAIT_BETWEEN_TRIES = 30
TEMP_DIR = gettempdir()


class YoutubeFile:
    def __init__(self, youtube_url, game_id):
        if not youtube_url:
            raise Exception("Youtube URL is blank")
        self.youtube_url = youtube_url
        self.game_id = game_id
        self.path = os.path.join(TEMP_DIR, self.game_id + '.mp4')

    def __enter__(self):
        tries = 0
        while True:
            try:
                ydl_opts = {
                    'outtmpl': self.path,
                    'format': '137',
                    'quiet': True,
                    'retries': MAX_RETIRES
                }
                with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([self.youtube_url])
                return self.path
            except (DLContentTooShortError, UrllibContentTooShortError) as e:
                tries += 1
                if tries >= MAX_RETIRES:
                    raise e
                time.sleep(WAIT_BETWEEN_TRIES)

    def __exit__(self, ex_type, value, traceback):
        os.remove(self.path)
        pass

if __name__ == "__main__":
    with YoutubeFile("https://www.youtube.com/watch?v=18zPvXjnCTI", "YoutubeFileTest") as video_path:
        print("DONE DOWNLOADING")
