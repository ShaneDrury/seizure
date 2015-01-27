import unittest
from seizure.lib.video import Video


class TestVideo(unittest.TestCase):
    def setUp(self):
        self.code = '3726758'
        # 3726758
        self.video = Video(self.code)
        # self.vod = {
        #     'chunks': {
        #         '360p': [{'url': 'url1'}, {'url': 'url2'}],
        #         'live': [{'url': 'url1'}, {'url': 'url2'}],
        #         '240p': [{'url': 'url1'}, {'url': 'url2'}],
        #         '480p': [{'url': 'url1'}, {'url': 'url2'}],
        #     }
        # }

    def test_get_best_quality(self):
        self.assertEqual(self.video.get_best_quality(), 'live')


if __name__ == '__main__':
    unittest.main()
