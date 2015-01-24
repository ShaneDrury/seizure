import unittest
from unittest.mock import patch, mock_open, MagicMock

from requests import HTTPError

from seizure.lib.download import download

m = mock_open()


class TestDownloads(unittest.TestCase):
    def test_file_exists(self):
        self.assertEqual(True, False)

    def test_url_doesnt_exist(self):
        self.assertRaises(HTTPError, download, 'http://testfoo.com/files/test.flv')

    @patch('seizure.lib.download.requests.get', autospec=True)
    @patch('seizure.lib.download.open', new=m, create=True)
    def test_download_to(self, mock_get):
        url = 'http://testfoo.com/files/test.flv'
        download(url)
        m.assert_called_with('test.flv', 'wb')
        download(url, to='bar.flv')
        m.assert_called_with('bar.flv', 'wb')


if __name__ == '__main__':
    unittest.main()
