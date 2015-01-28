import configparser
import json
import os
import logging


class Config(object):
    default_values = {
        'ffmpeg binary': 'ffmpeg',
        'download folder': '',
        'quality': 'live',
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
        logging.info('Writing initial config {}'.format(self.filename))
        self.config['DEFAULT'] = self.default_values
        with open(self.filename, 'w') as f:
            self.config.write(f)

    def update(self, key, value):
        self.config['DEFAULT'][key] = json.dumps(value)
        with open(self.filename, 'w') as f:
            self.config.write(f)

    @property
    def all_finished(self):
        return json.loads(self.config['DEFAULT']['finished'])

    @property
    def download_folder(self):
        return self.config['DEFAULT']['download folder']

    @property
    def ffmpeg_binary(self):
        return self.config['DEFAULT']['ffmpeg binary']

    @property
    def quality(self):
        return self.config['DEFAULT']['quality']
