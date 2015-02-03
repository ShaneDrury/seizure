import logging
import re
from urllib.parse import urlsplit
from seizure.lib.twitch import Twitch


class Video(object):
    def __init__(self, code: str, session):
        self.code = self.parse_code(code)
        self.twitch = Twitch(session)
        self.vod = self.twitch.request("api/videos/a{}".format(self.code))
        self.info = self.twitch.request(
            "kraken/videos/a{}?on_site=1".format(self.code)
        )

    def download_urls(self, quality):
        try:
            urls = [c['url'] for c in self.chunks[quality]]
        except KeyError:
            logging.error("{} doesn't exist. Choose from {}".
                          format(quality, list(self.qualities)))
            raise
        return urls

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

    def parse_code(self, code):
        if re.match('^\w+$', code):
            return code
        else:
            return urlsplit(code).path.split('/')[-1]
