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

    def assertDownloaded(self, magic_get):
        # TODO: Remove hard coded stuff
        calls = [call('url1', stream=True),
                 call().raise_for_status(),
                 call('url2', stream=True),
                 call().raise_for_status()]
        magic_get.assert_has_calls(calls)
        self.downloader.write_to_file.assert_has_calls([call(magic_get(), 'foo_2011-06-02t200403z_00.flv'),
                                                        call(magic_get(), 'foo_2011-06-02t200403z_01.flv')])

    @patch('seizure.lib.download.requests.get')
    def test_download(self, magic_get):
        expected = ['foo_2011-06-02t200403z_00.flv',
                    'foo_2011-06-02t200403z_01.flv']
        paths = self.downloader.download()
        self.assertDownloaded(magic_get)
        self.assertEqual(paths, expected)

    def test_download_folder(self):
        paths = self.downloader.download(folder='testfolder')
        expected = [os.path.join('testfolder', 'foo_2011-06-02t200403z_00.flv'),
                    os.path.join('testfolder', 'foo_2011-06-02t200403z_01.flv')]
        self.assertEqual(paths, expected)

    def test_download_chunk(self):
        self.downloader.download_chunk('url1', 'fname')
        self.assertEqual(True, False)

    def test_can_download_file(self):
        self.assertEqual(True, False)

    def test_write_to_file(self):
        self.assertEqual(True, False)

    def test_sanitize(self):
        self.assertEqual(True, False)

    def test_generate_filename(self):
        self.assertEqual(True, False)


if __name__ == '__main__':
    unittest.main()
