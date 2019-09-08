from datetime import datetime

from get_iplayer_python.bbc_dash_xml_extractor import get_stream_selection_xml
from get_iplayer_python.extractors.download_data_extractor import download_data_extractor
from get_iplayer_python.extractors.stream_template_extractor import get_stream_selection_links
from get_iplayer_python.helpers.sorted_extentions import sort_by_two_keys
from get_iplayer_python.models.Exceptions import MissingDataException



def get_best_download_template(vpid):
    output_data = {}

    # TODO: maybe in the future allow for which stream to download but for now the best one is chosen
    highest_quality_dash_stream = get_highest_quality_dash_stream(vpid)



    print("test")


def get_highest_quality_dash_stream(vpid):
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
    download_data = download_data_extractor("https://www.bbc.co.uk/programmes/b01dmw90", "./", True, [],
                                            datetime(1970, 1, 1))

    episode_data = download_data["episode_data"][0]

    get_best_download_template(episode_data["playlist_metadata"]["vpid"])
