from seizure.lib.twitch import Twitch


class Video(object):
    def __init__(self, url):
        self.url = url
        self.vod = Twitch.request(self.url)

    def download_urls(self):
        pass

    @property
    def chunks(self):
        return self.vod['chunks']

    @property
    def title(self):
        raise NotImplementedError()

    @property
    def game(self):
        raise NotImplementedError()

    @property
    def start_time(self):
        # Convert to datetime? maybe not needed
        raise NotImplementedError()


def get_best_quality(vod):
    available_qualities = vod['chunks'].keys()
    return sorted(available_qualities,
                  key=lambda x: Twitch.QUALITIES.index(x))[-1]
