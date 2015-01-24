import os
import requests

from seizure.lib.paths import rename_extension, files_from_vod, generate_filename
from seizure.lib.video import join_videos, convert_video


def requests_download_file(response, to):
    with open(to, 'wb') as f:
        for block in response.iter_content(1024):
            if not block:
                break
            f.write(block)


def download(url, to=None):
    to = to or url.split('/')[-1]
    if os.path.exists(to):
        raise IOError('{} exists'.format(to))
    response = requests.get(url, stream=True)
    response.raise_for_status()
    requests_download_file(response, to)


def download_vod(vod):
    video_urls = files_from_vod(vod)
    title, start_time, extension = vod.title, vod.start_time, vod.extension
    paths = [generate_filename(title, start_time, extension, n) for n in range(len(video_urls))]
    for vid, path in zip(video_urls, paths):
        download(vid, to=path)
    return paths


def convert_videos(paths):
    for saved in paths:
        convert_video(saved, to='mp4')
    converted_paths = [rename_extension(p, 'mp4') for p in paths]
    join_videos(converted_paths)
