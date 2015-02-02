import argparse
import logging
import os

from seizure.config import default_values
from seizure.lib.conversion import Converter
from seizure.lib.download import Downloader
from seizure.lib.downloadlog import DownloadLog
from seizure.lib.util import default_folder
from seizure.lib.video import Video


logging.basicConfig(level=logging.INFO)


def main():
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('code', metavar='code', type=str, help='VOD code')
    parser.add_argument('-quality', metavar='quality', type=str,
                        help='Quality of VOD: '
                             'One of 240p, 360p, 480p '
                             'and live.')
    parser.add_argument('-folder', metavar='folder', type=str,
                        help='Folder to download the VOD to.')
    parser.add_argument('-ffmpeg', metavar='ffmpeg', type=str,
                        help='Path to ffmpeg binary')
    parser.add_argument('-log', metavar='log', type=str,
                        help='Path to download log')
    args = parser.parse_args()
    quality = args.quality or default_values['quality']
    folder = args.folder or default_values['folder']
    ffmpeg = args.ffmpeg or default_values['ffmpeg']
    if not os.path.exists(ffmpeg):
        raise IOError("{} doesn't exist".format(ffmpeg))
    video = Video(args.code)
    download_log = args.log or default_folder(video)
    downloader = Downloader(video, DownloadLog(download_log))
    filenames = downloader.download(quality=quality, folder=folder)
    converter = Converter(ffmpeg)
    converted = converter.convert(filenames)
    logging.info("Converted {}".format(converted))

if __name__ == '__main__':
    main()
