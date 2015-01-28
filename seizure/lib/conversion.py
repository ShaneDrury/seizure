import os
import subprocess


class Converter(object):
    def __init__(self, ffmpeg_bin):
        self.ffmpeg = ffmpeg_bin

    def convert(self, paths, to='mp4'):
        save_to = self.joined_filename(paths)
        filelist = self.create_filelist(paths)
        tmp_filename = self.temp_filename(paths)
        with open(tmp_filename, 'w') as f:
            f.write(filelist)
            self.convert_and_join(tmp_filename, save_to)
        return save_to

    def create_filelist(self, paths):
        filelist = ''
        for f in paths:
            filelist += 'file \'{}\'\n'.format(f)
        return filelist

    def joined_filename(self, paths):
        """
        Assumes the paths are in the form {str}_{num}.{ext} e.g. path_01.mp4,
        path_02.mp4 etc. and returns path.mp4. Takes the first filename base.
        """
        base, ext = self.remove_digits(paths[0])
        return base + ext

    def temp_filename(self, paths):
        base, _ = self.remove_digits(paths[0])
        return base + '.tmp'

    def convert_and_join(self, filelist, save_to):
        subprocess.check_call([self.ffmpeg, '-f', 'concat', '-i', filelist,
                               '-c', 'copy', save_to])

    @staticmethod
    def remove_digits(path):
        base, ext = os.path.splitext(path)
        last_underscore = base.rindex('_')
        return base[:last_underscore], ext

    @staticmethod
    def rename_extension(path, extension):
        ext = os.path.splitext(path)[1].split('.')[-1]
        return path.replace(ext, extension)
