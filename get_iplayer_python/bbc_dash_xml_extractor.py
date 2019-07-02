from random import randint

import requests


def get_stream_selection_xml(vpid: str):
    ch = random_of_set_length(5)
    url = "https://open.live.bbc.co.uk/mediaselector/5/select/version/2.0/mediaset/iptv-all/vpid"
    return requests.get(f"{url}/{vpid}?cb={ch}")


def random_of_set_length(number_of_digets):
    range_start = 10**(number_of_digets-1)
    range_end = (10**number_of_digets)-1
    return randint(range_start, range_end)

