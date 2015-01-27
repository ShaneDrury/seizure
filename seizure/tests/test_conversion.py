import unittest

from seizure.lib.conversion import Converter


class TestPaths(unittest.TestCase):
    def setUp(self):
        pass

    def test_rename_extension(self):
        renamed = Converter.rename_extension('foo.flv', 'mp4')
        self.assertEqual(renamed, 'foo.mp4')

    def test_rename_extension_path(self):
        renamed = Converter.rename_extension('/tmp/seizure/foo.flv', 'mp4')
        self.assertEqual(renamed, '/tmp/seizure/foo.mp4')

    def test_convert(self):
        self.assertEqual(True, False)

    def test_convert_one(self):
        self.assertEqual(True, False)

    def test_join(self):
        self.assertEqual(True, False)