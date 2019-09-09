from datetime import datetime

from get_iplayer_python.extractors.bbc_dash_xml_extractor import get_stream_selection_xml
from get_iplayer_python.extractors.download_data_extractor import download_data_extractor
from get_iplayer_python.extractors.stream_template_extractor import get_stream_selection_links, create_templates
from get_iplayer_python.helpers.sorted_extentions import sort_by_two_keys
from get_iplayer_python.models.Exceptions import MissingDataException


def get_best_download_templates(vpid, audio_only):
    """
    For a given vpid get the best quality templates for each filetype e.g. audio and video
    :param vpid:
    :param audio_only: only audio if you are only interested in audio
    :return:
    """
    # TODO: maybe in the future allow for which stream to download but for now the best one is chosen
    highest_quality_dash_stream = get_highest_quality_dash_stream(vpid)

    all_templates = create_templates(highest_quality_dash_stream["href"])

    periods_by_filetype = [
        group_period_representations_by_file_type(period, audio_only)
        for period in all_templates["periods"]
    ]

    periods_best_templates = [
        get_highest_bandwidth_item(period)
        for period in periods_by_filetype
    ]

    download_templates_avalible = all(
        [
            bool(template_dict)
            for template_dict in periods_best_templates
        ]
    )

    if not download_templates_avalible:
        MissingDataException(f"no download templates available for vpid: {vpid}")

    return periods_best_templates


def get_highest_bandwidth_item(periods_by_filetype_dict):
    """
    for a given period get the best templates for each file type
    :param periods_by_filetype_dict:
    :return: {
        "audio": { adaptaion, representation, period }
    }
    """
    output = {}
    for filetype, templates in periods_by_filetype_dict.items():
        output[filetype] = sorted(templates, key=lambda x: int(x["representation"]["bandwidth"]), reverse=True)[0]

    return output


def group_period_representations_by_file_type(period_dict, audio_only):
    """
    order data fromo create_templates function by type
    this is meant to be run on one period
    e.g. audio and video
    :param period_dict:
    :param audio_only: only return templates that are audio (if you're downloading audio only)
    :return:
    """
    templates_by_filetype = {}
    for adaptation in period_dict["adaptation_sets"]:
        for representation in adaptation["representations"]:
            filetype = representation["mimetype"].split("/")[0]

            if audio_only and filetype != "audio":
                continue

            if filetype not in templates_by_filetype:
                templates_by_filetype[filetype] = []

            templates_by_filetype[filetype].append(
                {
                    "period": period_dict,
                    "adaptation_set": adaptation,
                    "representation": representation
                }
            )

    return templates_by_filetype


def get_highest_quality_dash_stream(vpid):
    """
    The first page linked to when downloading from BBC is an XML doc that has a link to a bunch of DASH
    XML Documents. This function gets the best of those XML documents based upon highest bitrate and priority
    :param vpid:
    :return: best fit DASH XML
    """
    # get links to available download dash streams
    stream_selection_xml = get_stream_selection_xml(vpid)
    stream_selection_links = get_stream_selection_links(stream_selection_xml.content)

    highest_to_lowest_quality_streams = sorted(
        stream_selection_links,
        key=sort_by_two_keys("priority", "bitrate"),
        reverse=True
    )

    if not any(highest_to_lowest_quality_streams):
        raise MissingDataException("no dash streams available for this URL")

    return highest_to_lowest_quality_streams[0]


if __name__ == '__main__':
    download_data = download_data_extractor("https://www.bbc.co.uk/programmes/b0bx2rj3", "./", True, [],
                                            datetime(1970, 1, 1))
    # download_data = download_data_extractor("https://www.bbc.co.uk/programmes/b01dmw90", "./", True, [],
    #                                         datetime(1970, 1, 1))
    episode_data = download_data["episode_data"][0]

    get_best_download_templates(episode_data["playlist_metadata"]["vpid"], True)
