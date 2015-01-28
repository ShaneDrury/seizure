import unittest

from seizure.lib.conversion import Converter


class TestConversion(unittest.TestCase):
    """
    Note, we are not testing ffmpeg, just the interface of the class.
    """
    def setUp(self):
        self.paths = ['path_01.flv', 'path_02.flv']
        self.converter = Converter('ffmpeg')

    def test_rename_extension(self):
        renamed = Converter.rename_extension('foo.flv', 'mp4')
        self.assertEqual(renamed, 'foo.mp4')

    def test_rename_extension_path(self):
        renamed = Converter.rename_extension('/tmp/seizure/foo.flv', 'mp4')
        self.assertEqual(renamed, '/tmp/seizure/foo.mp4')

    def test_convert(self):
        converted = self.converter.convert(self.paths, to='mp4')
        self.assertEqual(converted, 'path.mp4')
