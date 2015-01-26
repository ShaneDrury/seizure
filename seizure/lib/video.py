from seizure.lib.twitch import Twitch


class Video(object):
    def __init__(self, url: str):
        self.url = url
        self.vod = Twitch.request(self.url)

    def download_urls(self, quality):
        return [c['url'] for c in self.chunks[quality]]

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

    @property
    def qualities(self):
        return self.chunks.keys()

    @property
    def extension(self):
        """Assume they're all the same"""
        url = self.chunks[self.get_best_quality()][0]
        return url.split('.')[-1]

    def get_best_quality(self):
        return sorted(self.qualities, key=lambda x: Twitch.QUALITIES.index(x))[-1]
