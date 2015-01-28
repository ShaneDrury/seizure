import unittest
from unittest.mock import MagicMock, patch

from seizure.lib.conversion import Converter


class TestConversion(unittest.TestCase):
    """
    Note, we are not testing ffmpeg, just the interface of the class.
    """

    def setUp(self):
        self.paths = ['path_01.flv', 'path_02.flv']
        self.converter = Converter('ffmpeg')
        self.converter.convert_and_join = MagicMock()

    def test_rename_extension(self):
        renamed = Converter.rename_extension('foo.flv', 'mp4')
        self.assertEqual(renamed, 'foo.mp4')

    def test_rename_extension_path(self):
        renamed = Converter.rename_extension('/tmp/seizure/foo.flv', 'mp4')
        self.assertEqual(renamed, '/tmp/seizure/foo.mp4')

    def test_convert(self):
        converted = self.converter.convert(self.paths)
        self.assertEqual(converted, 'path.mp4')

    def test_skip_conversion(self):
        self.converter.convert(self.paths)
        with patch('seizure.lib.conversion.os.path.exists',
                   return_value=True):
            self.assertRaises(OSError, self.converter.convert, self.paths)
