import re
import unicodedata


def sanitize(value):
    value = unicodedata.normalize('NFKD', value). \
        encode('ascii', 'ignore').decode('ascii')
    value = re.sub('[^\w\s-]', '', value).strip().lower()
    return re.sub('[-\s]+', '-', value)


def default_folder(vod):
    return sanitize('{}'.format(vod.title))
