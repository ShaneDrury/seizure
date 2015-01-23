from seizure.lib.paths import generate_path, rename_extension
from seizure.lib.video import join_videos, convert_video


def download(url, to=None):
    pass

all_videos = []

paths = [generate_path(video) for video in all_videos]
video_urls = [video.url for video in all_videos]
for vid, path in zip(video_urls, paths):
    download(vid, to=path)

for saved in paths:
    convert_video(saved, to='mp4')

converted_paths = [rename_extension(p, 'mp4') for p in paths]
join_videos(converted_paths)