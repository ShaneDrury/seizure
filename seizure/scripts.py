import argparse
import logging

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
                             'and live')
    args = parser.parse_args()
    config = Config(args.config)
    quality = args.quality or config.quality
    video = Video(args.code)
    downloader = Downloader(video, config)
    filenames = downloader.download(quality=quality,
                                    folder=config.download_folder)
    converter = Converter(config.ffmpeg_binary)
    converted = converter.convert(filenames)
    logging.info("Converted {}".format(converted))

if __name__ == '__main__':
    main()
