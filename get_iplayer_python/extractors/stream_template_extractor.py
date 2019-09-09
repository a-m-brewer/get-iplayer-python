import math
import re
from datetime import timedelta

import requests
from bs4 import BeautifulSoup


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
    """
    get templates for downloading context as a python dict. this gets all the information required to get
    content.
    :param url: dash xml url
    :param xml_getter_function:
    :return: dict
    """

    mpd_data = dash_xml_to_dict(url, xml_getter_function)

    for period in mpd_data["periods"]:
        for adaptation_set in period["adaptation_sets"]:
            for representation in adaptation_set["representations"]:
                r_id = representation["xml"].attrs["id"]
                info = adaptation_set["adaptation_information"]

                segment_duration = float(info["segment_duration"]) * 1 / info["timescale"]
                period_duration = get_seconds_duration(period["xml"].attrs["duration"])
                total_segments = int(math.ceil(float(period_duration) / segment_duration))

                representation["bandwidth"] = r_id.split("=")[1]
                representation["mimetype"] = adaptation_set["xml"].attrs["mimetype"]

                # create the filename of the initialisation segment
                representation["initialisation_template_url"] = info["initialization"].replace(
                    "$RepresentationID$",
                    r_id
                )

                # a template url for each of the segments in the download
                representation["segment_template_url"] = (
                    info["media"]
                    .replace("$RepresentationID$", r_id)
                    .replace("$Number$", "%(Number)d")
                )

                """
                MEDIA SEGMENTS:
                The actual media files. these files are sections of the whole. generally played back as if it were
                one file.
                e.g. Diplo and Friends is usually split into about 570 segments. each being about 6.4 minutes of the
                show
                """
                representation["download_segments"] = [
                    {
                        "path": representation["segment_template_url"] % {
                            'Number': segment_number,
                            'Bandwidth': representation["bandwidth"]
                        },
                        "duration": segment_duration
                    }
                    for segment_number in range(info["start_number"], total_segments + info["start_number"])
                ]

    return mpd_data


def dash_xml_to_dict(url: str, xml_getter_function=xml_getter_func):
    """
    Get and convert the DASH XML document into a python dict. with following content

    :PERIOD:
    top level MPEG Dash component includes start time and duration
    used for scenes / chapters in movies

    :ADAPTATION SET:
    An adaptation set is a media stream related to the content
    e.g. common example is a TV show would likely have one video adaptation set
    and multiple audio adaptation sets e.g. different languages

    :REPRESENTATION:
    Allows for adaptation sets to be encoded in different ways
    for example different qualities of audio or different codecs

    :param url:
    :param xml_getter_function:
    :return: dict
    """
    base_url_path = get_url_path(url)

    xml = xml_getter_function(url)
    soup = BeautifulSoup(xml, 'lxml')

    return {
        "periods": [
            {
                "xml": period,
                "adaptation_sets": [
                    {
                        "xml": adaptation_set,
                        "adaptation_information": get_adaption_info(adaptation_set),
                        "representations": [
                            {
                                "xml": representation,
                                "base_dash_path": f"{base_url_path}"
                                f"{get_dash_path_extension(representation, adaptation_set, period)}"
                            }
                            for representation in adaptation_set.findAll("representation")
                        ]
                    }
                    for adaptation_set in period.findAll("adaptationset")
                ]
            }
            for period in soup.html.body.mpd.findAll("period")
        ]
    }


def get_url_path(url):
    """
    Get the base url of the MPD file
    e.g. www.website.com/mpd/file.mpd
    would return www.website.com/mpd/
    :param url: MPD download link
    :return: str
    """
    return url.rpartition('/')[0] + "/"


def get_dash_path_extension(representation, adaptation, period):
    """
    Get the extension to the base path for the DASH items
    :param representation: representation set
    :param adaptation: adaptation set
    :param period: adaptation period
    :return: gets the extension of the for dash file
    """
    result = ""
    for xml_element in (representation, adaptation, period):
        possible_extension = xml_element.find('baseurl')
        if possible_extension is not None:
            result = f"{possible_extension.text}{result}"
            if re.match(r'^https?://', result):
                break
    return result


def get_seconds_duration(time_string):
    """
    convert PT1H59.989333S into seconds
    :param time_string: e.g. PT1H59.989333S
    :return: seconds
    """
    def get_time_delta(time_unit: str):
        time_item = re.findall(r'[0-9.]+|$', time_unit)[0]
        unit = re.findall(r'[A-Z]|$', time_unit)[0]
        if unit == "D":
            return timedelta(days=float(time_item))
        if unit == "H":
            return timedelta(hours=float(time_item))
        if unit == "M":
            return timedelta(minutes=float(time_item))
        if unit == "S":
            return timedelta(seconds=float(time_item))

    time = re.findall(r'[0-9.]+[A-Z]', time_string)
    return sum([get_time_delta(item) for item in time], timedelta(0)).total_seconds()


def get_adaption_info(adaptation_set):
    segment_template = adaptation_set.find("segmenttemplate")
    return {
        "start_number": 1,
        "timescale": int(segment_template["timescale"]),
        "segment_duration": float(segment_template["duration"]),
        "media": segment_template["media"],
        "initialization": segment_template["initialization"]
    }


if __name__ == '__main__':
    create_templates(
        "https://aod-dash-uk-live.bbcfmt.hs.llnwd.net/usp/auth/vod/piff_abr_full_audio/7ea78b-m000883q/vf_m000883q_37331a1e-64e7-43d2-80ec-c2afbe7a6339.ism.hlsv2.ism/iptv_hd_abr_v1_uk_dash_master.mpd?s=1567915774&e=1567958974&h=ba5b572d93810c569d013d21f4662cd2")
