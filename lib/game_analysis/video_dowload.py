import os


class YoutubeFile:
    def __init__(self, youtube_url, game_id):
        if not youtube_url:
            raise Exception("Youtube URL is blank")
        self.youtube_url = youtube_url
        self.game_id = game_id

    def __enter__(self):
        self.path = '/tmp/%s.mp4' % self.game_id
        os.system("youtube-dl -f 137 -o '" + self.path + "' -q " + self.youtube_url)
        return self.path

    def __exit__(self, type, value, traceback):
        os.system("rm -f " + self.path)
        pass
