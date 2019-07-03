import argparse

from get_iplayer_python.bbc_iplayer_downloader import download_from_url
import logging


def args():
    parser = argparse.ArgumentParser()
    parser.add_argument("url")
    parser.add_argument("-a","--audio-only", help="only download audio from stream", action="store_true", default=False)
    parser.add_argument("-l", "--download-location", help="download location of items", type=str, default="./")
    parser.add_argument("-o", "--overwrite",
                        help="overwrite existing downloads in download folder", action="store_true", default=False)
    return parser.parse_args()


def main():
    logging.basicConfig(level=logging.DEBUG, format="[%(asctime)s][%(levelname)s]: %(message)s")
    logging.getLogger('urllib3.connectionpool').setLevel(logging.ERROR)
    program_args = args()
    download_from_url(program_args.url,
                      program_args.download_location,
                      overwrite=program_args.overwrite,
                      audio_only=program_args.audio_only)


if __name__ == '__main__':
    main()
