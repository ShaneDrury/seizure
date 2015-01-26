import os


class Converter(object):
    def __init__(self, ffmpeg_bin):
        self.ffmpeg = ffmpeg_bin

    def convert(self, paths, to='mp4'):
        for saved in paths:
            self.convert_one_video(saved, to='mp4')
        converted_paths = [self.rename_extension(p, 'mp4') for p in paths]
        self.join(converted_paths)

    def convert_one_video(self, file, to='mp4'):
        pass

    @staticmethod
    def rename_extension(path, extension):
        ext = os.path.splitext(path)[1].split('.')[-1]
        return path.replace(ext, extension)

    def join(self, paths):
        pass
