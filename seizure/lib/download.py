import os
import logging
import re
import unicodedata

import requests

from seizure.lib.config import Config
from seizure.lib.video import Video

logger = logging.getLogger(__name__)


class Downloader(object):
    def __init__(self, vod: Video, config: Config):
        self.vod = vod
        self.config = config

    def download(self, quality=None, folder=''):
        quality = quality or self.vod.get_best_quality()
        video_urls = self.vod.download_urls(quality)
        filenames = [os.path.join(folder, self.generate_filename(n))
                     for n, url in enumerate(video_urls)]
        for v, f in zip(video_urls, filenames):
            if self.can_download_file(f):
                self.download_chunk(v, f)
        return filenames

    def download_chunk(self, url, to):
        to = to or url.split('/')[-1]
        response = requests.get(url, stream=True)
        response.raise_for_status()
        self.write_to_file(response, to)

    def can_download_file(self, filename):
        return not self.config.finished(filename)

    @staticmethod
    def write_to_file(response, to):
        with open(to, 'wb') as f:
            for block in response.iter_content(1024):
                if not block:
                    break
                f.write(block)

    @staticmethod
    def sanitize(value):
        value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
        value = re.sub('[^\w\s-]', '', value).strip().lower()
        return re.sub('[-\s]+', '-', value)

    def generate_filename(self, num):
        title = self.sanitize(self.vod.title)
        t = self.sanitize(self.vod.start_time)
        num = str(num).zfill(2)
        return "{}_{}_{}.{}".format(title, t, num, self.vod.extension)
