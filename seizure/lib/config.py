import configparser


class Config(object):
    def __init__(self, filename):
        self.filename = filename
        self.config = configparser.ConfigParser()
        self.config.read(filename)

    def started(self, filename):
        """Has the filename been started?"""
        return filename in self.config['STARTED']

    def finished(self, filename):
        """Has the filename been started?"""
        return filename in self.config['FINISHED']

    def write_initial(self):
        self.config['STARTED'] = ['', ]
        self.config['FINISHED'] = ['', ]
        with open(self.filename, 'w') as f:
            self.config.write(f)
