import unittest
from unittest.mock import patch
from seizure.lib.paths import rename_extension, generate_filename


class TestPaths(unittest.TestCase):
    @patch('seizure.lib.video.Video', title='Test Title', extension='flv', start_time='2011-10-02T19:57:06Z')
    def test_generate_filename(self, video):
        path = generate_filename(video)
        self.assertEqual(path, 'test-title_2011-10-02t195706z.flv')

    def test_rename_extension(self):
        renamed = rename_extension('foo.flv', 'mp4')
        self.assertEqual(renamed, 'foo.mp4')

    def test_rename_extension_path(self):
        renamed = rename_extension('/tmp/seizure/foo.flv', 'mp4')
        self.assertEqual(renamed, '/tmp/seizure/foo.mp4')


if __name__ == '__main__':
    unittest.main()
