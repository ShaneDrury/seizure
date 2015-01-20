class Twitch(object):
    """
    Consume Twitch API.
    """
    def __init__(self):
        pass


class REST(object):
    def __init__(self, api):
        self.api = api

    def get(self, *args, **kwargs):
        raise NotImplementedError()
