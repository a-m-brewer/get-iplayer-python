from get_iplayer_python.bbc_iplayer_downloader import download_from_url
import logging


def main():
    logging.basicConfig(level=logging.DEBUG, format="[%(asctime)s][%(levelname)s]: %(message)s")
    logging.getLogger('urllib3.connectionpool').setLevel(logging.ERROR)
    download_from_url("https://www.bbc.co.uk/programmes/b01dmw90/episodes/player", "./")


if __name__ == '__main__':
    main()
