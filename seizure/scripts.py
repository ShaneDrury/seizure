import argparse
import logging
import os

from requests import Session

from seizure.config import default_values
from seizure.lib.conversion import Converter
from seizure.lib.download import Downloader
from seizure.lib.downloadlog import DownloadLog
from seizure.lib.util import default_folder
from seizure.lib.video import Video


logging.basicConfig(level=logging.INFO)


def main():
    parser = argparse.ArgumentParser(
        description='Download Twitch VODs.',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        argument_default=argparse.SUPPRESS
    )
    parser.add_argument('code', metavar='code', type=str, help='VOD code',
                        nargs='+')
    parser.add_argument('-q', '--quality', metavar='quality', type=str,
                        default=default_values['quality'],
                        help='quality of VOD: 240p, 360p, 480p, live')
    parser.add_argument('-f', '--folder', metavar='folder', type=str,
                        default=default_values['folder'],
                        help='folder to download the VOD to; defaults to the '
                             'current working directory')
    parser.add_argument('-m', '--ffmpeg', metavar='ffmpeg', type=str,
                        default=default_values['ffmpeg'],
                        help='path to ffmpeg binary')
    parser.add_argument('-l', '--log', metavar='log', type=str,
                        help='path to download log (default: '
                             '{FOLDER}/{VOD_TITLE}/download.log)')
    args = parser.parse_args()
    if not os.path.exists(args.ffmpeg):
        raise IOError("{} doesn't exist".format(args.ffmpeg))
    for code in args.code:
        with Session() as session:
            video = Video(code, session)
            try:
                download_log = args.log
            except AttributeError:
                download_log = os.path.join(args.folder, default_folder(video),
                                            'download.log')
            downloader = Downloader(video, DownloadLog(download_log), session)
            filenames = downloader.download(
                quality=args.quality,
                folder=os.path.join(
                    args.folder, default_folder(video)
                )
            )
        converter = Converter(args.ffmpeg)
        converted = converter.convert(filenames)
        logging.info("Converted {}".format(converted))
        for file in filenames:
            logging.info("Removing {}".format(file))
            os.remove(file)

if __name__ == '__main__':
    main()
