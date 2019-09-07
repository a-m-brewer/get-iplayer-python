import argparse

from datetime import datetime

from get_iplayer_python.bbc_iplayer_downloader import download_from_url
import logging


def args():
    parser = argparse.ArgumentParser()
    parser.add_argument("url")
    parser.add_argument("-a", "--audio-only", help="only download audio from stream", action="store_true", default=False)
    parser.add_argument("-d", "--after-date", help="download items only after date format '%Y-%m-%d %H:%M:%S'",
                        type=lambda s: datetime.strptime(s, '%Y-%m-%d %H:%M:%S'),
                        default=datetime(1970, 1, 1))
    parser.add_argument("-l", "--download-location", help="download location of items", type=str, default="./")
    parser.add_argument("-o", "--overwrite",
                        help="overwrite existing downloads in download folder", action="store_true", default=False)
    parser.add_argument("--output-format", help="output format of the show e.g. mp3, mkv", default=None)
    return parser.parse_args()


def main():
    logging.basicConfig(level=logging.DEBUG, format="[%(asctime)s][%(levelname)s]: %(message)s")
    logging.getLogger('urllib3.connectionpool').setLevel(logging.ERROR)
    program_args = args()
    download_from_url(program_args.url,
                      program_args.download_location,
                      overwrite=program_args.overwrite,
                      audio_only=program_args.audio_only,
                      after_date=program_args.after_date,
                      output_format=program_args.output_format)


if __name__ == '__main__':
    main()
