import re
from datetime import datetime

from dateutil.parser import parse

import requests

from get_iplayer_python.is_bbc_re import IS_BBC_URL_RE

DEFAULT_DATETIME_STRING = '1970-01-01T00:00:00Z'


def requests_get_metadata_json(url: str):
    return requests.get(url).json()


def get_pid_from_url(url):
    search_item = re.compile(IS_BBC_URL_RE)
    match = search_item.match(url)
    return match.group("id")


def get_show_playlist_data(url: str, json_getter=requests_get_metadata_json):
    pid = get_pid_from_url(url)
    full_json = json_getter(f"http://www.bbc.co.uk/programmes/{pid}/playlist.json")
    image_url = "http:%s" % full_json["holdingImage"].replace("\\", "")
    return {
        "image_url": image_url,
        "pid": full_json["defaultAvailableVersion"]["pid"],
        "title": full_json["defaultAvailableVersion"]["smpConfig"]["title"],
        "vpid": full_json["defaultAvailableVersion"]["smpConfig"]["items"][0]["vpid"],
        "duration": full_json["defaultAvailableVersion"]["smpConfig"]["items"][0]["duration"]
    }


def get_show_metadata(url: str, json_getter=requests_get_metadata_json):
    pid = get_pid_from_url(url)
    full_json = json_getter(f"https://www.bbc.co.uk/programmes/{pid}.json")["programme"]

    first_broadcast_date_json = full_json.get('first_broadcast_date', DEFAULT_DATETIME_STRING)
    first_broadcast_date = DEFAULT_DATETIME_STRING if first_broadcast_date_json is None else first_broadcast_date_json

    return {
        "title": full_json["title"],
        "display_title": full_json["display_title"],
        "pid": full_json["pid"],
        "image_pid": full_json["image"]["pid"],
        "first_broadcast_date": parse(first_broadcast_date)
    }

