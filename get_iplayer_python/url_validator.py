import re
from json import JSONDecodeError

import tldextract as tldextract

from get_iplayer_python.bbc_metadata_generator import get_show_metadata
from get_iplayer_python.is_bbc_re import IS_BBC_URL_RE

url_regex = re.compile(
    r'^(?:http|ftp)s?://'  # http:// or https://
    # domain...
    r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'
    r'localhost|'  # localhost...
    r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
    r'(?::\d+)?'  # optional port
    r'(?:/?|[/?]\S+)$', re.IGNORECASE)


pid_regex = re.compile(
    r"/programmes/[a-z0-9]{8}"
)

programmes_regex = re.compile(
    r".*programmes.*"
)


def is_episode_page(url: str):
    try:
        meta = get_show_metadata(url)
    except JSONDecodeError:
        return False
    return meta["display_title"]["subtitle"] != ""


def is_programme_page(url):
    try:
        meta = get_show_metadata(url)
    except JSONDecodeError:
        return False
    return meta["display_title"]["subtitle"] == "" and not url.endswith("/episodes/player")


def is_playlist_page(url: str):
    try:
        get_show_metadata(url)
    except JSONDecodeError:
        return True
    return False


def is_bbc_url(url: str):
    return re.match(IS_BBC_URL_RE, url) is not None


def is_programmes_url(url: str):
    return is_bbc_url(url) and __has_programme(url)


def __has_programme(url: str):
    return re.match(programmes_regex, url) is not None


def __is_url(url: str):
    result = re.match(url_regex, url) is not None
    return result


def __has_pid(url: str):
    result = re.search(pid_regex, url)
    return bool(result)


def __is_bbc_domain(url: str):
    return __get_domain(url) == "bbc"


def __get_domain(url: str):
    return tldextract.extract(url).domain
