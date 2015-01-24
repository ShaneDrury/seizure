import unittest
from unittest.mock import patch

from requests import HTTPError

from seizure.lib.download import download


class TestDownloads(unittest.TestCase):
    @patch('seizure.lib.download.os.path.exists', return_value=True)
    def test_file_exists(self, mock_exists):
        self.assertRaises(OSError, download, 'http://testfoo.com/files/test.flv')

    def test_url_doesnt_exist(self):
        self.assertRaises(HTTPError, download, 'http://testfoo.com/files/test.flv')

    @patch('seizure.lib.download.requests.get', autospec=True)
    @patch('seizure.lib.download.open', create=True)
    def test_download_to(self, my_mock_open, mock_get):
        url = 'http://testfoo.com/files/test.flv'
        download(url)
        my_mock_open.assert_called_with('test.flv', 'wb')
        mock_get.assert_called_with(url, stream=True)
        download(url, to='bar.flv')
        my_mock_open.assert_called_with('bar.flv', 'wb')
        mock_get.assert_called_with(url, stream=True)


if __name__ == '__main__':
    unittest.main()
