import os


class DownloadLog(object):
    def __init__(self, filename):
        self.filename = filename
        self.log = self.get_log(filename)

    @staticmethod
    def get_log(filename):
        if os.path.exists(filename):
            with open(filename, 'r') as f:
                return [line.rstrip('\n') for line in f]
        else:
            return []

    def write_log(self):
        with open(self.filename, 'w') as f:
            for line in self.log:
                f.write(line + '\n')

    def update(self, filename):
        self.log.append(filename)
        self.write_log()

    def remove(self, filename):
        self.log.remove(filename)
        self.write_log()

    def finished(self, filename):
        return filename in self.log
