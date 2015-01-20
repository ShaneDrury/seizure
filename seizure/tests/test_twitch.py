import unittest

from requests import HTTPError

from seizure.lib.twitch import api


class TestChannels(unittest.TestCase):
    def setUp(self):
        self.api = api

    def test_get_channel(self):
        """
        A lot of keys in the response are not guaranteed to be constant, so
        we have to get rid of them before comparing equality.
        """
        response = self.api.channel.get('test_user1')
        to_pop = ['updated_at', 'background', 'video_banner', 'banner',
                  'mature', 'status', 'display_name', 'game', 'teams', 'logo']
        for k in to_pop:
            response.pop(k)
        expected = {
            "_links": {
                "videos": "https://api.twitch.tv/kraken/channels/test_user1/"
                          "videos",
                "self": "https://api.twitch.tv/kraken/channels/test_user1",
                "follows": "https://api.twitch.tv/kraken/channels/test_user1/"
                           "follows",
                "commercial": "https://api.twitch.tv/kraken/channels/"
                              "test_user1/commercial",
                "stream_key": "https://api.twitch.tv/kraken/channels/"
                              "test_user1/stream_key",
                "chat": "https://api.twitch.tv/kraken/chat/test_user1",
                "features": "https://api.twitch.tv/kraken/channels/test_user1/"
                            "features",
                "subscriptions": "https://api.twitch.tv/kraken/channels/"
                                 "test_user1/subscriptions",
                "editors": "https://api.twitch.tv/kraken/channels/test_user1/"
                           "editors"
            },
            "url": "http://www.twitch.tv/test_user1",
            "_id": 22747064,
            "name": "test_user1",
            "created_at": "2011-06-02T20:04:03Z",
        }
        self.assertDictEqual(response, expected)

    def test_channel_doesnt_exist(self):
        self.assertRaises(HTTPError, self.api.channel.get, 'doesnotexist')


if __name__ == '__main__':
    unittest.main()
