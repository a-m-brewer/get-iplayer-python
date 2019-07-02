import math
import re
from datetime import timedelta

import requests
from bs4 import BeautifulSoup

base_info = {
    'start_number': 1,
    'timescale': 1,
}


def get_stream_selection_links(dash_xml_page_string):
    xml = BeautifulSoup(dash_xml_page_string, 'lxml')
    media_selection = xml.html.body.mediaselection
    media_parts = media_selection.findAll("media")
    dash_links_details = []
    for media in media_parts:
        connections = media.findAll("connection")
        media_hrefs = [
            {"href": con.attrs["href"], "priority": con.attrs["priority"], "bitrate": media.attrs["bitrate"]}
            for con in connections if "transferformat" in con.attrs and con.attrs["transferformat"] == "dash"
        ]
        dash_links_details.extend(media_hrefs)

    return dash_links_details


def xml_getter_func(url):
    return requests.get(url).text


def create_templates(url: str, xml_getter_function=xml_getter_func):
    orig_url = url.rpartition('/')[0] + "/"
    periods = get_programme_periods(url, xml_getter_function)
    download_items = []
    for period in periods:
        adaptation_sets = get_programme_adaptation_sets(period)
        for a_set in adaptation_sets:
            information = get_adaption_info(a_set)
            representations = get_programme_representation(a_set)
            mime_type = a_set.attrs["mimetype"]
            for rep in representations:

                base_url = ''
                for element in (rep, a_set, period):
                    base_url_e = element.find('baseurl')
                    if base_url_e is not None:
                        base_url = base_url_e.text + base_url
                        if re.match(r'^https?://', base_url):
                            break

                full_dash_url = orig_url + base_url

                init_template = prepare_initialization_template(information["initialization"], rep.attrs["id"])
                media_template = prepare_media_template(information["media"], rep.attrs["id"])

                bandwidth = rep.attrs["id"].split("=")[1]

                fragments = create_fragments(
                    "path",
                    information["start_number"],
                    calculate_number_of_segments(
                        information["segment_duration"],
                        get_seconds_duration(period.attrs["duration"]),
                        information["timescale"]
                    ),
                    get_real_segment_duration(information["segment_duration"], information["timescale"]),
                    bandwidth,
                    media_template
                )

                download_items.append({
                    "base_url": full_dash_url,
                    "init_url": init_template,
                    "fragments": fragments,
                    "bandwidth": bandwidth,
                    "mimetype": mime_type
                })
    return download_items


def get_programme_duration(url: str, xml_getter):
    xml = get_parsed_xml(url, xml_getter)
    mpd = xml.html.body.mpd.attrs["mediapresentationduration"]
    return get_seconds_duration(mpd)


def get_seconds_duration(time_string):
    time = re.findall(r'[0-9.]+[A-Z]', time_string)
    return sum([get_time_delta(item) for item in time], timedelta(0)).total_seconds()


def get_programme_periods(url: str, xml_getter):
    xml = get_parsed_xml(url, xml_getter)
    return xml.html.body.mpd.findAll("period")


def get_programme_adaptation_sets(periods_xml):
    return periods_xml.findAll("adaptationset")


def get_programme_representation(adaptation_xml):
    return adaptation_xml.findAll("representation")


def get_adaption_info(adaptation_set):
    segment_template = adaptation_set.find("segmenttemplate")
    result = base_info.copy()
    result["timescale"] = int(segment_template["timescale"])
    result["segment_duration"] = float(segment_template["duration"])
    result["media"] = segment_template["media"]
    result["initialization"] = segment_template["initialization"]
    return result


def prepare_media_template(media_url, representation_id):
    result = media_url.replace("$RepresentationID$", representation_id)
    return result.replace("$Number$", "%(Number)d")


def prepare_initialization_template(init_url, representation_id):
    return init_url.replace("$RepresentationID$", representation_id)


def create_fragments(media_location_key, start_fragment_number, total_fragment_number, segment_duration, bandwidth, media_template):
    return [
        {
            media_location_key: media_template % {
                'Number': segment_number,
                'Bandwidth': bandwidth
            },
            "duration": segment_duration
        }
        for segment_number in range(start_fragment_number, total_fragment_number + start_fragment_number)
    ]


def get_parsed_xml(url: str, xml_getter):
    xml = xml_getter(url)
    return BeautifulSoup(xml, 'lxml')


def calculate_number_of_segments(segment_duration, period_duration, timescale):
    seg_dur = get_real_segment_duration(segment_duration, timescale)
    return int(math.ceil(float(period_duration) / seg_dur))


def get_real_segment_duration(segment_duration, timescale):
    return float(segment_duration) * 1 / timescale


def get_time_delta(time_unit: str):
    time = re.findall(r'[0-9.]+|$', time_unit)[0]
    unit = re.findall(r'[A-Z]|$', time_unit)[0]
    if unit == "D":
        return timedelta(days=float(time))
    if unit == "H":
        return timedelta(hours=float(time))
    if unit == "M":
        return timedelta(minutes=float(time))
    if unit == "S":
        return timedelta(seconds=float(time))


if __name__ == '__main__':
    create_templates()