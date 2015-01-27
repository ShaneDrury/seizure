import os
import unittest

from seizure.lib.config import Config


class TestConfig(unittest.TestCase):
    def setUp(self):
        self.fname = 'testconfig.ini'
        self.config = Config(self.fname)
        self.config.update('finished', ['path1', 'path2'])

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
