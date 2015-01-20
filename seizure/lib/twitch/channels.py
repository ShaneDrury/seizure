from urllib.parse import urljoin
from seizure.lib.twitch.base import Resource


class ChannelV2(Resource):
    base_path = 'channels/'

    def get(self, name):
        url = urljoin(self.base_path, name)
        return self.api.get(url)
