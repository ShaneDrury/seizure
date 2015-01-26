from functools import partial
import os
import logging

import requests

from seizure.lib.paths import rename_extension, files_from_vod, generate_filename, get_extension
from seizure.lib.video import join_videos, convert_video, get_best_quality

logger = logging.getLogger(__name__)


class Downloader(object):
    def __init__(self, vod):
        self.vod = vod

    def download(self, quality=None, to=None):
        pass


def requests_download_file(response, to):
    with open(to, 'wb') as f:
        for block in response.iter_content(1024):
            if not block:
                break
            f.write(block)


def download(url, to=None):
    to = to or url.split('/')[-1]
    response = requests.get(url, stream=True)
    response.raise_for_status()
    requests_download_file(response, to)


def download_vod(vod, quality=None):
    quality = quality or get_best_quality(vod)
    video_urls = files_from_vod(vod, quality=quality)
    title, start_time = vod['title'], vod['start_time']
    extensions = [get_extension(url) for url in video_urls]
    gen_fname = partial(generate_filename, title, start_time)
    paths = [gen_fname(ext, n) for n, ext in enumerate(extensions)]
    for vid, path in zip(video_urls, paths):
        if os.path.exists(path):
            if vid in vod['started']:
                logger.info("Redownloading {}".format(vid))
                download(vid, to=path)
            else:
                logger.info("Already downloaded {}".format(vid))
        else:
            logger.info("Downloading {}".format(vid))
            download(vid, to=path)
    return paths


def convert_videos(paths):
    for saved in paths:
        convert_video(saved, to='mp4')
    converted_paths = [rename_extension(p, 'mp4') for p in paths]
    join_videos(converted_paths)
