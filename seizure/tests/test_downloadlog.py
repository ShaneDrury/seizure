import os
import unittest

from seizure.lib.downloadlog import DownloadLog


class TestConfig(unittest.TestCase):
    def setUp(self):
        self.fname = 'testlog.log'
        self.config = DownloadLog(self.fname)
        self.config.update('path1')
        self.config.update('path2')

    def tearDown(self):
        os.remove(self.fname)

    def test_finished(self):
        self.assertTrue(self.config.finished('path1') and
                        self.config.finished('path2') and not
                        self.config.finished('pathdoesnotexist'))

    def test_write_initial(self):
        self.assertTrue(os.path.exists(self.fname))


if __name__ == '__main__':
    unittest.main()
