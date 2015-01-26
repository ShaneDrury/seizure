import unittest
from unittest.mock import patch

from requests import HTTPError

from seizure.lib.download import download, download_vod


class TestDownloads(unittest.TestCase):
    def setUp(self):
        self.vod = {'chunks': {'240p': [{'url': 'url1'}, {'url': 'url2'}]},
                    'title': 'test title',
                    'start_time': '2011-10-02T19:57:06Z',
                    'started': [None, ]}
        self.url = 'http://testfoo.com/files/test.flv'

    @patch('seizure.lib.download.logger')
    def test_skip_file(self, mock_logger):
        download_vod(self.vod)
        mock_logger.assert_called_with('Already downloaded url1')

    def test_url_doesnt_exist(self):
        self.assertRaises(HTTPError, download, self.url)

    @patch('seizure.lib.download.requests.get', autospec=True)
    @patch('seizure.lib.download.open', create=True)
    def test_download_to(self, mock_open, mock_get):
        download(self.url)
        mock_open.assert_called_with('test.flv', 'wb')
        mock_get.assert_called_with(self.url, stream=True)
        download(self.url, to='bar.flv')
        mock_open.assert_called_with('bar.flv', 'wb')

    @patch('seizure.lib.download.logger')
    @patch('seizure.lib.download.requests.get', autospec=True)
    @patch('seizure.lib.download.os.path.exists', return_value=True)
    @patch('seizure.lib.download.open', create=True)
    def test_redownload(self, mock_open, mock_exists, mock_get, mock_logger):
        self.vod['started'] = ['url1', ]
        download_vod(self.vod)
        mock_logger.assert_called_with('Redownloading url1')
        mock_open.assert_called_with('test.flv', 'wb')
        mock_get.assert_called_with(self.url, stream=True)

    @patch('seizure.lib.download.logger')
    @patch('seizure.lib.download.requests.get', autospec=True)
    @patch('seizure.lib.download.os.path.exists', return_value=False)
    @patch('seizure.lib.download.open', create=True)
    def test_download_vod(self, mock_open, mock_exists, mock_get, mock_logger):
        download_vod(self.vod)
        mock_logger.assert_called_with('Downloading url1')
        mock_open.assert_called_with('test.flv', 'wb')
        mock_get.assert_called_with(self.url, stream=True)


if __name__ == '__main__':
    unittest.main()
