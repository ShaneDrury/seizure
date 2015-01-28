import argparse
from seizure.lib.config import Config
from seizure.lib.download import Downloader
from seizure.lib.video import Video


def main():
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('code', metavar='code', type=str, help='VOD code')

    args = parser.parse_args()
    video = Video(args.code)
    config = Config('config.ini')
    downloader = Downloader(video, config)
    downloader.download(quality=config.quality,
                        folder=config.download_folder)

if __name__ == '__main__':
    main()
