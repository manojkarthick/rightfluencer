from __future__ import unicode_literals
import youtube_dl


class MyLogger(object):
    def debug(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        print(msg)


def my_hook(d):
    print(d)
    if d['status'] == 'finished':
        print('Done downloading, now converting ...')


ydl_opts = {
    'verbose': True,
    'skip_download': True,
    'logger': MyLogger(),
    'progress_hooks': [my_hook],
    'subtitleslangs': 'en',
    'writeautomaticsub': True,
}


with youtube_dl.YoutubeDL(ydl_opts) as ydl:
    ydl.download(['https://www.youtube.com/watch?v=Ye8mB6VsUHw'])