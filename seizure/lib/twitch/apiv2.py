from urllib.parse import urljoin

import requests

from seizure.lib.twitch.base import Twitch
from seizure.lib.twitch.channels import ChannelV2


class TwitchAPIV2(Twitch):
    """
    Version 2
    """
    mime_type = 'application/vnd.twitchtv.v2+json'
    base_url = 'https://api.twitch.tv/kraken/'

    def __init__(self):
        super(TwitchAPIV2, self).__init__()
        self.channel = ChannelV2(self)

    def get(self, url, *args, **kwargs):
        full_url = urljoin(self.base_url, url)
        response = requests.get(full_url, headers={'Accept': self.mime_type})
        self.validate_response(response)
        return self._to_json(response.text)
