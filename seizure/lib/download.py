import os
import logging

from progressbar import ProgressBar, Bar, FileTransferSpeed, Percentage

from seizure.lib.downloadlog import DownloadLog
from seizure.lib.util import sanitize
from seizure.lib.video import Video


class Downloader(object):
    def __init__(self, vod: Video, log: DownloadLog, session):
        self.vod = vod
        self.log = log
        self.session = session

    def download(self, quality=None, folder=None):
        quality = quality or self.vod.get_best_quality()
        folder = folder or ''
        video_urls = self.vod.download_urls(quality)
        if not os.path.exists(folder):
            os.makedirs(folder)
        filenames = [os.path.join(folder, self.generate_filename(n, quality))
                     for n, url in enumerate(video_urls)]
        for n, (v, f) in enumerate(zip(video_urls, filenames)):
            fraction = "{}/{}".format(n+1, len(filenames))
            if self.can_download_file(f):
                logging.info("Downloading {} {}".format(fraction, v))
                self.download_chunk(v, f)
            else:
                logging.info("Skipping {} {}".format(fraction, v))
        return filenames

    def download_chunk(self, url, to):
        to = to or self.default_filename(url)
        response = self.session.get(url, stream=True)
        response.raise_for_status()
        self.write_to_file(response, to)
        self.log.update(to)

    @staticmethod
    def default_filename(url):
        return url.split('/')[-1]

    def can_download_file(self, filename):
        if not os.path.exists(filename) and self.log.finished(filename):
            self.log.remove(filename)
            return True
        return not self.log.finished(filename)

    @staticmethod
    def write_to_file(response, to):
        widgets = [Bar(), Percentage(), ' ', FileTransferSpeed()]
        with ProgressBar(widgets=widgets,
                         maxval=int(response.headers['Content-Length'])) \
                as pbar:
            with open(to, 'wb') as f:
                for n, block in enumerate(response.iter_content(1024)):
                    if not block:
                        break
                    f.write(block)
                    pbar.update(n * 1024)

    def generate_filename(self, num, quality):
        title = sanitize(self.vod.title)
        t = sanitize(self.vod.start_time)
        num = str(num).zfill(2)
        return "{}_{}_{}_{}.{}".format(title, t, quality, num,
                                       self.vod.extension)
