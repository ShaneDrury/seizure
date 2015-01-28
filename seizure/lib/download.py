import os
import logging
import re
import unicodedata
from progressbar import SimpleProgress, ProgressBar, AnimatedMarker, Bar

import requests

from seizure.lib.config import Config
from seizure.lib.video import Video

logger = logging.getLogger(__name__)


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
        for v, f in zip(video_urls, filenames):
            if self.can_download_file(f):
                self.download_chunk(v, f)
        return filenames

    def default_folder(self):
        return self.sanitize('{}'.format(self.vod.title))

    def download_chunk(self, url, to):
        to = to or self.default_filename(url)
        response = requests.get(url, stream=True)
        response.raise_for_status()
        self.write_to_file(response, to)
        finished = self.config.all_finished()
        finished.append(to)
        self.config.update('finished', finished)

    def default_filename(self, url):
        return url.split('/')[-1]

    def can_download_file(self, filename):
        return not self.config.finished(filename)

    @staticmethod
    def write_to_file(response, to):
        pbar = ProgressBar(widgets=[Bar()],
                           maxval=int(response.headers['Content-Length'])/1024)
        pbar.start()
        with open(to, 'wb') as f:
            for n, block in enumerate(response.iter_content(1024)):
                if not block:
                    break
                f.write(block)
                pbar.update(n+1)
        pbar.finish()

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
