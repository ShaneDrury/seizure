import os
import subprocess
import tempfile


class Converter(object):
    def __init__(self, ffmpeg_bin):
        self.ffmpeg = ffmpeg_bin

    def convert(self, paths):
        save_to = self.rename_extension(self.joined_filename(paths), 'mp4')
        if os.path.exists(save_to):
            return save_to
        filelist = self.create_filelist(paths)
        with tempfile.NamedTemporaryFile() as f:
            f.write(filelist)
            f.seek(0)
            f.flush()
            self.convert_and_join(f.name, save_to)
        return save_to

    @staticmethod
    def create_filelist(paths):
        filelist = ''
        for f in paths:
            filelist += 'file \'{}\'\n'.format(os.path.abspath(f))
        return bytes(filelist, 'UTF-8')

    def joined_filename(self, paths):
        """
        Assumes the paths are in the form {str}_{num}.{ext} e.g. path_01.mp4,
        path_02.mp4 etc. and returns path.mp4. Takes the first filename base.
        """
        base, ext = self.remove_digits(paths[0])
        return base + ext

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
