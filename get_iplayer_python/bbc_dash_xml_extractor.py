from random import randint

import requests

from get_iplayer_python.bbc_metadata_generator import get_show_playlist_data


def get_stream_selection_xml(vpid: str):
    ch = random_of_set_length(5)
    url = "https://open.live.bbc.co.uk/mediaselector/5/select/version/2.0/mediaset/iptv-all/vpid"
    return requests.get(f"{url}/{vpid}?cb={ch}")


def random_of_set_length(number_of_digets):
    range_start = 10**(number_of_digets-1)
    range_end = (10**number_of_digets)-1
    return randint(range_start, range_end)


if __name__ == '__main__':
    vpid = get_show_playlist_data("https://www.bbc.co.uk/programmes/m000669y")["vpid"]
    result = get_stream_selection_xml(vpid)
    print(result.content)
