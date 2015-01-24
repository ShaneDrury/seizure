from seizure.lib.paths import rename_extension, files_from_vod, generate_filename
from seizure.lib.video import join_videos, convert_video


def download(url, to=None):
    pass


def download_multiple_videos(all_videos):
    for vod in all_videos:
        download_vod(vod)


def download_vod(vod):
    video_urls = files_from_vod(vod)
    title, start_time, extension = vod.title, vod.start_time, vod.extension
    paths = [generate_filename(title, start_time, extension, n) for n in range(len(video_urls))]
    for vid, path in zip(video_urls, paths):
        download(vid, to=path)
    for saved in paths:
        convert_video(saved, to='mp4')
    converted_paths = [rename_extension(p, 'mp4') for p in paths]
    join_videos(converted_paths)
