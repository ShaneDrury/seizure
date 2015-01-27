import os


class Converter(object):
    def __init__(self, ffmpeg_bin):
        self.ffmpeg = ffmpeg_bin

    def convert(self, paths, to='mp4'):
        for saved in paths:
            self.convert_one_video(saved, to)
        converted_paths = [self.rename_extension(p, to) for p in paths]
        return self.join(converted_paths)

    def convert_one_video(self, file, to='mp4'):
        pass

    @staticmethod
    def rename_extension(path, extension):
        ext = os.path.splitext(path)[1].split('.')[-1]
        return path.replace(ext, extension)

    @staticmethod
    def joined_filename(paths):
        """
        Assumes the paths are in the form {str}_{num}.{ext} e.g. path_01.mp4,
        path_02.mp4 etc. and returns path.mp4. Takes the first filename base.
        """
        base, ext = os.path.splitext(paths[0])
        last_underscore = base.rindex('_')
        return base[:last_underscore] + ext

    def join(self, paths):
        return self.joined_filename(paths)
