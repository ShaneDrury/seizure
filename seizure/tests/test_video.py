import unittest

from seizure.lib.video import Video
from seizure.tests.util import skip_if_local


class TestVideo(unittest.TestCase):
    def setUp(self):
        self.code = '609886511'
        self.video = Video(self.code)

    @skip_if_local('slow')
    def test_get_best_quality(self):
        self.assertEqual(self.video.get_best_quality(), 'live')

    @skip_if_local('slow')
    def test_chunks(self):
        for k, v in self.video.chunks.items():
            self.assertIsInstance(v, list)

    @skip_if_local('slow')
    def test_title(self):
        self.assertEqual(self.video.title,
                         '#AGDQ2015 Benefiting the Prevent Cancer Foundation')

    @skip_if_local('slow')
    def test_game(self):
        self.assertEqual(self.video.game, 'Super Smash Bros. Melee')

    @skip_if_local('slow')
    def test_start_time(self):
        self.assertEqual(self.video.start_time, '2015-01-11T18:07:25Z')

    @skip_if_local('slow')
    def test_qualities(self):
        self.assertEqual(sorted(self.video.qualities),
                         ['240p', '360p', '480p', 'live'])

    @skip_if_local('slow')
    def test_extension(self):
        self.assertEqual(self.video.extension, 'flv')


if __name__ == '__main__':
    unittest.main()
