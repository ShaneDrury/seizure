import configparser
import os


class Config(object):
    default_values = {
        'ffmpeg binary': 'ffmpeg',
        'download folder': '.',
        'finished': ['', ],
        }

    def __init__(self, filename):
        self.filename = filename
        self.config = configparser.ConfigParser()
        self.config.read(filename)
        if not os.path.exists(self.filename):
            self.write_initial()

    def finished(self, filename):
        """Has the filename been started?"""
        return filename in self.config['DEFAULT']['finished']

    def write_initial(self):
        self.config['DEFAULT'] = self.default_values
        with open(self.filename, 'w') as f:
            self.config.write(f)

    def update(self, key, value):
        self.config['DEFAULT'][key] = str(value)
        with open(self.filename, 'w') as f:
            self.config.write(f)
