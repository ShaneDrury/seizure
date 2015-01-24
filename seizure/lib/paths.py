import os
import re
import unicodedata


def sanitize(value):
    value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
    value = re.sub('[^\w\s-]', '', value).strip().lower()
    return re.sub('[-\s]+', '-', value)


def files_from_vod(vod, quality=None):
    try:
        chunks = vod['chunks'][quality]
    except KeyError:
        raise ValueError('{} not found for {}'.format(quality, vod['title']))
    return [c['url'] for c in chunks]


def generate_filename(title, start_time, extension, num):
    title = sanitize(title)
    t = sanitize(start_time)
    num = str(num).zfill(2)
    return "{}_{}_{}.{}".format(title, t, num, extension)


def rename_extension(path, extension):
    ext = os.path.splitext(path)[1].split('.')[-1]
    return path.replace(ext, extension)
