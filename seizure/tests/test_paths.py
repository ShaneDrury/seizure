import unittest
from seizure.lib.paths import rename_extension


class TestPaths(unittest.TestCase):
    def test_generate_path(self):
        self.assertEqual(True, False)

    def test_rename_extension(self):
        renamed = rename_extension('foo.flv', 'mp4')
        self.assertEqual(renamed, 'foo.mp4')

        renamed = rename_extension('/tmp/seizure/foo.flv', 'mp4')
        self.assertEqual(renamed, '/tmp/seizure/foo.mp4')


if __name__ == '__main__':
    unittest.main()
