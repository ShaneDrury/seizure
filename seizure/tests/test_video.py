import unittest
from seizure.lib.video import get_best_quality


class TestVideo(unittest.TestCase):
    def setUp(self):
        self.vod = {
            'chunks': {
                '360p': [{'url': 'url1'}, {'url': 'url2'}],
                'live': [{'url': 'url1'}, {'url': 'url2'}],
                '240p': [{'url': 'url1'}, {'url': 'url2'}],
                '480p': [{'url': 'url1'}, {'url': 'url2'}],
            }
        }

    def test_get_best_quality(self):
        self.assertEqual(get_best_quality(self.vod), 'live')


if __name__ == '__main__':
    unittest.main()
