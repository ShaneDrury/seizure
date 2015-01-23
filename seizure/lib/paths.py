import os
import re
import unicodedata


def sanitize(value):
    value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
    value = re.sub('[^\w\s-]', '', value).strip().lower()
    return re.sub('[-\s]+', '-', value)


def generate_filename(video):
    title = sanitize(video.title)
    t = sanitize(video.start_time)
    extension = video.extension
    return "{}_{}.{}".format(title, t, extension)


def rename_extension(path, extension):
    ext = os.path.splitext(path)[1].split('.')[-1]
    return path.replace(ext, extension)
