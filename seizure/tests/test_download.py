import os
import unittest
from unittest.mock import MagicMock, patch, call

from seizure.lib.download import Downloader


class TestDownloader(unittest.TestCase):
    def setUp(self):
        self.vod = MagicMock()
        self.config = MagicMock()
        self.config.finished.return_value = False
        self.vod.get_best_quality.return_value = '240p'
        self.vod.title = 'Foo'
        self.vod.start_time = '2011-06-02T20:04:03Z'
        self.vod.extension = 'flv'
        self.vod.download_urls.return_value = ['url1', 'url2']
        # noinspection PyTypeChecker
        self.downloader = Downloader(self.vod, self.config)
        self.downloader.write_to_file = MagicMock()

    def assertDownloaded(self, magic_get, urls, expected_calls):
        calls = []
        for url in urls:
            calls.append(call(url, stream=True))
            calls.append(call().raise_for_status())
        magic_get.assert_has_calls(calls)
        self.downloader.write_to_file.assert_has_calls(expected_calls)

    @patch('seizure.lib.download.requests.get')
    def test_download(self, magic_get):
        expected = ['foo_2011-06-02t200403z_00.flv',
                    'foo_2011-06-02t200403z_01.flv']
        paths = self.downloader.download()
        calls = [call(magic_get(), 'foo_2011-06-02t200403z_00.flv'),
                 call(magic_get(), 'foo_2011-06-02t200403z_01.flv')]
        self.assertDownloaded(magic_get, self.vod.download_urls.return_value,
                              calls)
        self.assertEqual(paths, expected)

    @patch('seizure.lib.download.requests.get')
    def test_download_folder(self, magic_get):
        paths = self.downloader.download(folder='testfolder')
        expected = [os.path.join('testfolder', 'foo_2011-06-02t200403z_00.flv'),
                    os.path.join('testfolder', 'foo_2011-06-02t200403z_01.flv')]
        calls = [call(magic_get(), 'testfolder/foo_2011-06-02t200403z_00.flv'),
                 call(magic_get(), 'testfolder/foo_2011-06-02t200403z_01.flv')]
        self.assertDownloaded(magic_get, self.vod.download_urls.return_value,
                              calls)
        self.assertEqual(paths, expected)

    @patch('seizure.lib.download.requests.get')
    def test_download_chunk(self, magic_get):
        self.downloader.download_chunk('url1', 'fname')
        self.assertDownloaded(magic_get, ['url1'], [call(magic_get(), 'fname')])

    def test_default_filename(self):
        self.assertEqual(
            self.downloader.default_filename(
                'http://www.testsite.com/vods/vod789798f.flv'
            ),
            'vod789798f.flv'
        )

    def test_can_download_file(self):
        self.assertEqual(self.downloader.can_download_file('fname'), True)
        self.config.finished.return_value = True
        self.assertEqual(self.downloader.can_download_file('fname'), False)

    def test_sanitize(self):
        sanitized = self.downloader.sanitize('TEStStriNG-:::4&^$%324"8.')
        self.assertEqual(sanitized, 'teststring-43248')

    def test_generate_filename(self):
        fname = self.downloader.generate_filename(1)
        self.assertEqual(fname, 'foo_2011-06-02t200403z_01.flv')
        fname = self.downloader.generate_filename(99)
        self.assertEqual(fname, 'foo_2011-06-02t200403z_99.flv')
        fname = self.downloader.generate_filename(999)
        self.assertEqual(fname, 'foo_2011-06-02t200403z_999.flv')


if __name__ == '__main__':
    unittest.main()
