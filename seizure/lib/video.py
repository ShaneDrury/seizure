from seizure.lib.twitch import QUALITIES


def get_best_quality(vod):
    available_qualities = vod['chunks'].keys()
    return sorted(available_qualities, key=lambda x: QUALITIES.index(x))[-1]


def join_videos(paths):
    pass


def convert_video(path, to=None):
    pass
