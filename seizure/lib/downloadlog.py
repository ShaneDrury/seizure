import os
import csv


class DownloadLog(object):
    def __init__(self, filename):
        self.filename = filename
        self.log = self.get_log(filename)

    def get_log(self, filename):
        if os.path.exists(filename):
            with open(filename, 'r') as f:
                return list(csv.reader(f))
        else:
            return []

    def write_log(self):
        with open(self.filename, 'w') as f:
            writer = csv.writer(f)
            for url in self.log:
                writer.writerow(url)

    def update(self, url):
        self.log.append(url)
        self.write_log()

    def remove(self, url):
        self.log.remove(url)
        self.write_log()

    def finished(self, url):
        return url in self.log