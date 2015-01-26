import unittest


class TestPaths(unittest.TestCase):
    def test_generate_filename(self):
        path = generate_filename('Test Title', '2011-10-02T19:57:06Z', 'flv', 1)
        self.assertEqual(path, 'test-title_2011-10-02t195706z_01.flv')

    def test_rename_extension(self):
        renamed = rename_extension('foo.flv', 'mp4')
        self.assertEqual(renamed, 'foo.mp4')

    def test_rename_extension_path(self):
        renamed = rename_extension('/tmp/seizure/foo.flv', 'mp4')
        self.assertEqual(renamed, '/tmp/seizure/foo.mp4')

    def test_get_extension(self):
        self.assertEqual(get_extension('http://testfoo.com/files/test.flv'), 'flv')


class TestFilesVod(unittest.TestCase):
    def test_get_urls(self):
        expected = ['url1', 'url2']
        vod = {'chunks': {'240p': [{'url': 'url1'}, {'url': 'url2'}]}}
        urls = files_from_vod(vod, quality='240p')
        self.assertEqual(urls, expected)

    def test_quality_doesnt_exist(self):
        vod = {'chunks': {'240p': None}, 'title': 'test title'}
        self.assertRaises(ValueError, files_from_vod, vod, quality='doesntexist')


if __name__ == '__main__':
    unittest.main()
