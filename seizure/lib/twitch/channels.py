from seizure.lib.twitch.base import REST


class Channels(REST):
    def get(self, name):
        request = 'foo'
        self.api.get_channel(request)
