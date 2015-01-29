import argparse
import logging
import os

from seizure.lib.config import Config
from seizure.lib.conversion import Converter
from seizure.lib.download import Downloader
from seizure.lib.video import Video

logging.basicConfig(level=logging.INFO)


def main():
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('code', metavar='code', type=str, help='VOD code')
    parser.add_argument('--config', metavar='config', type=str,
                        default='config.ini', help='Config file')
    parser.add_argument('-quality', metavar='quality', type=str,
                        help='Quality of VOD: '
                             'One of 240p, 360p, 480p '
                             'and live.')
    parser.add_argument('-folder', metavar='folder', type=str,
                        help='Folder to download the VOD to.')
    parser.add_argument('-ffmpeg', metavar='ffmpeg', type=str,
                        help='Path to ffmpeg binary')
    args = parser.parse_args()
    config = Config(args.config)
    quality = args.quality or config.quality
    folder = args.folder or config.download_folder
    ffmpeg = args.ffmpeg or config.ffmpeg_binary
    if not os.path.exists(ffmpeg):
        raise IOError("{} doesn't exist".format(ffmpeg))
    video = Video(args.code)
    downloader = Downloader(video, config)
    filenames = downloader.download(quality=quality,
                                    folder=folder)
    converter = Converter(ffmpeg)
    converted = converter.convert(filenames)
    logging.info("Converted {}".format(converted))

if __name__ == '__main__':
    main()
