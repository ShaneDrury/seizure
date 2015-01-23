import json
from urllib.parse import urljoin

import requests

BASE_URL = 'https://api.twitch.tv/kraken/'
MIME_TYPE = 'application/vnd.twitchtv.v2+json'


def request(resource, **kwargs):
    headers = {'Accept': MIME_TYPE}
    response = requests.get(urljoin(BASE_URL, resource),
                            headers=headers, **kwargs)
    response.raise_for_status()
    return json.loads(response.text)
