from urllib.parse import urljoin

import requests


class Twitch(object):
    BASE_URL = 'https://api.twitch.tv/'
    MIME_TYPE = 'application/vnd.twitchtv.v2+json'
    QUALITIES = ['240p', '360p', '480p', 'live']

    @classmethod
    def request(cls, resource, **kwargs):
        headers = {'Accept': cls.MIME_TYPE}
        response = requests.get(urljoin(cls.BASE_URL, resource),
                                headers=headers, **kwargs)
        response.raise_for_status()
        return response.json()
