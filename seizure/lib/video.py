from seizure.lib.twitch import Twitch


class Video(object):
    def __init__(self, code: str):
        self.code = code
        self.vod = Twitch.request("api/videos/a{}".format(self.code))
        self.info = Twitch.request(
            "kraken/videos/a{}?on_site=1".format(self.code)
        )

    def download_urls(self, quality):
        return [c['url'] for c in self.chunks[quality]]

    @property
    def chunks(self):
        return self.vod['chunks']

    @property
    def title(self):
        return self.info['title']

    @property
    def game(self):
        return self.info['game']

    @property
    def start_time(self):
        return self.info['recorded_at']

    @property
    def qualities(self):
        return self.chunks.keys()

    @property
    def extension(self):
        """Assume they're all the same"""
        url = self.chunks[self.get_best_quality()][0]['url']
        return url.split('.')[-1]

    def get_best_quality(self):
        return sorted(self.qualities,
                      key=lambda x: Twitch.QUALITIES.index(x))[-1]
