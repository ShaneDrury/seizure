from urllib.parse import urljoin


class Twitch(object):
    BASE_URL = 'https://api.twitch.tv/'
    MIME_TYPE = 'application/vnd.twitchtv.v2+json'
    QUALITIES = ['240p', '360p', '480p', 'live']

    def __init__(self, session):
        self.session = session

    def request(self, resource, **kwargs):
        headers = {'Accept': self.MIME_TYPE}
        response = self.session.get(urljoin(self.BASE_URL, resource),
                                    headers=headers, **kwargs)
        response.raise_for_status()
        return response.json()
