import os
import re
import unicodedata
import logging

import requests
from progressbar import ProgressBar, Bar, FileTransferSpeed, Percentage

from seizure.lib.config import Config
from seizure.lib.video import Video


class Downloader(object):
    def __init__(self, vod: Video, config: Config):
        self.vod = vod
        self.config = config

    def download(self, quality=None, folder=None):
        quality = quality or self.vod.get_best_quality()
        folder = folder or self.default_folder()
        video_urls = self.vod.download_urls(quality)
        if not os.path.exists(folder):
            os.makedirs(folder)
        filenames = [os.path.join(folder, self.generate_filename(n))
                     for n, url in enumerate(video_urls)]
        for n, (v, f) in enumerate(zip(video_urls, filenames)):
            fraction = "{}/{}".format(n+1, len(filenames))
            if self.can_download_file(f):
                logging.info("Downloading {} {}".format(fraction, v))
                self.download_chunk(v, f)
            else:
                logging.info("Skipping {} {}".format(fraction, v))
        return filenames

    def default_folder(self):
        return self.sanitize('{}'.format(self.vod.title))

    def download_chunk(self, url, to):
        to = to or self.default_filename(url)
        response = requests.get(url, stream=True)
        response.raise_for_status()
        self.write_to_file(response, to)
        finished = self.config.all_finished
        finished.append(to)
        self.config.update('finished', finished)

    def default_filename(self, url):
        return url.split('/')[-1]

    def can_download_file(self, filename):
        if not os.path.exists(filename) and self.config.finished(filename):
            finished = self.config.all_finished
            finished.remove(filename)
            self.config.update('finished', finished)
            return True
        return not self.config.finished(filename)

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

    @staticmethod
    def sanitize(value):
        value = unicodedata.normalize('NFKD', value). \
            encode('ascii', 'ignore').decode('ascii')
        value = re.sub('[^\w\s-]', '', value).strip().lower()
        return re.sub('[-\s]+', '-', value)

    def generate_filename(self, num):
        title = self.sanitize(self.vod.title)
        t = self.sanitize(self.vod.start_time)
        num = str(num).zfill(2)
        return "{}_{}_{}.{}".format(title, t, num, self.vod.extension)
