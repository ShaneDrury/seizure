import json


class Twitch(object):
    """
    Consume Twitch API.
    """
    def __init__(self):
        pass

    def _to_json(self, content):
        return json.loads(content)

    def validate_response(self, response):
        response.raise_for_status()


class Resource(object):
    def __init__(self, api):
        self.api = api