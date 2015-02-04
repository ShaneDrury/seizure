import os
import unittest
from unittest.mock import MagicMock, patch, call

from seizure.lib.download import Downloader
from seizure.lib.util import sanitize


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
        self.session = MagicMock()
        # self.session.get = MagicMock()
        # noinspection PyTypeChecker
        self.downloader = Downloader(self.vod, self.config, self.session)
        self.downloader.write_to_file = MagicMock()
        os.makedirs('testfolder')

    def tearDown(self):
        os.removedirs('testfolder')

    def assertDownloaded(self, magic_get, urls, expected_calls):
        calls = []
        for url in urls:
            calls.append(call(url, stream=True))
            calls.append(call().raise_for_status())
        magic_get.assert_has_calls(calls)
        # noinspection PyUnresolvedReferences
        self.downloader.write_to_file.assert_has_calls(expected_calls)

    def test_download_folder(self):
        paths = self.downloader.download(folder='testfolder')
        expected = [
            os.path.join('testfolder', 'foo_2011-06-02t200403z_240p_00.flv'),
            os.path.join('testfolder', 'foo_2011-06-02t200403z_240p_01.flv')
        ]
        calls = [call(self.session.get(),
                      'testfolder/foo_2011-06-02t200403z_240p_00.flv'),
                 call(self.session.get(),
                      'testfolder/foo_2011-06-02t200403z_240p_01.flv')]
        self.assertDownloaded(self.session.get,
                              self.vod.download_urls.return_value, calls)
        self.assertEqual(paths, expected)

    def test_download_chunk(self):
        self.downloader.download_chunk('url1', 'fname')
        self.assertDownloaded(self.session.get, ['url1'],
                              [call(self.session.get(), 'fname')])

    def test_default_filename(self):
        self.assertEqual(
            self.downloader.default_filename(
                'http://www.testsite.com/vods/vod789798f.flv'
            ),
            'vod789798f.flv'
        )

    @patch('seizure.lib.download.os.path.exists', return_value=True)
    def test_can_download_file(self, mock_exists):
        self.assertEqual(self.downloader.can_download_file('fname'), True)
        self.config.finished.return_value = True

        self.assertEqual(self.downloader.can_download_file('fname'), False)

    def test_sanitize(self):
        sanitized = sanitize('TEStStriNG-:::4&^$%324"8.')
        self.assertEqual(sanitized, 'teststring-43248')

    def test_generate_filename(self):
        fname = self.downloader.generate_filename(1, 'live')
        self.assertEqual(fname, 'foo_2011-06-02t200403z_live_01.flv')
        fname = self.downloader.generate_filename(99, '240p')
        self.assertEqual(fname, 'foo_2011-06-02t200403z_240p_99.flv')
        fname = self.downloader.generate_filename(999, '360p')
        self.assertEqual(fname, 'foo_2011-06-02t200403z_360p_999.flv')


if __name__ == '__main__':
    unittest.main()
