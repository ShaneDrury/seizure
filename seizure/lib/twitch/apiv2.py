from seizure.lib.twitch.base import Twitch


class TwitchAPIV2(Twitch):
    """
    Version 2
    """
    mime_type = 'application/vnd.twitchtv.v2+json'
    base_url = ''

    def get(self, *args, **kwargs):
        pass

    def get_channel(self, name):
        self.get()
