from seizure.lib.twitch import Twitch


class Video(object):
    def __init__(self, code: str):
        self.code = code
        # videos/a{id_}'
        # /kraken/videos/a{id_}?on_site=1'
        self.vod = Twitch.request("videos/a{}".format(self.code), kraken=False)
        self.info = Twitch.request("videos/{}?onsite=1".format(self.code))
        print(self.vod)
        print(self.info)
        print(self.code)

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
        return sorted(self.qualities,
                      key=lambda x: Twitch.QUALITIES.index(x))[-1]
