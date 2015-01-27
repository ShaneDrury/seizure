import unittest
from seizure.lib.config import Config
from seizure.lib.download import Downloader
from seizure.lib.video import Video


class TestPaths(unittest.TestCase):
    def setUp(self):
        pass

    def test_rename_extension(self):
        renamed = self.downloader.rename_extension('foo.flv', 'mp4')
        self.assertEqual(renamed, 'foo.mp4')

    def test_rename_extension_path(self):
        renamed = rename_extension('/tmp/seizure/foo.flv', 'mp4')
        self.assertEqual(renamed, '/tmp/seizure/foo.mp4')