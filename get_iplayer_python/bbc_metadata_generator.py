import requests


def requests_get_metadata_json(url: str):
    return requests.get(url).json()


def get_show_playlist_data(url: str, json_getter=requests_get_metadata_json):
    full_json = json_getter(f"{url}/playlist.json")
    image_url = "http:%s" % full_json["holdingImage"].replace("\\", "")
    return {
        "image_url": image_url,
        "vpid": full_json["defaultAvailableVersion"]["smpConfig"]["items"][0]["vpid"]
    }


def get_show_metadata(url: str, json_getter=requests_get_metadata_json):
    full_json = json_getter(f"{url}.json")["programme"]
    return {
        "display_title": full_json["display_title"],
        "pid": full_json["pid"],
        "image_pid": full_json["image"]["pid"]
    }
