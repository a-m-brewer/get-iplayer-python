from datetime import datetime, timedelta

import pytz
from simplejson.errors import JSONDecodeError

from get_iplayer_python.bbc_metadata_generator import get_show_metadata, get_show_playlist_data
from get_iplayer_python.extractors.bbc_link_extractor import extract_bbc_links
from get_iplayer_python.models.Exceptions import ArgumentException, UserInputException
from get_iplayer_python.models.SourceUrlType import SourceUrlType
from get_iplayer_python.url_validator import is_bbc_url


def download_data_extractor(url, location, audio, download_hooks, after_date):
    """
    Gets all the data required to ready in order to download the episodes related to the given URL
    :throws: ArgumentException, UserInputException
    :param url: source url
    :param location: location of download
    :param audio: download as audio
    :param download_hooks: list of action<obj>
    :param after_date: minimum first broadcast date of episodes
    :return: dict
    """

    output_data = {}

    if not is_bbc_url(url):
        raise UserInputException(f"{url} is not a valid BBC URl")

    output_data["source_url"] = url
    output_data["location"] = location if location.endswith("/") else f"{location}/"
    output_data["audio"] = audio

    if not isinstance(download_hooks, list):
        raise ArgumentException("download hooks must be a list of functions taking one parameter")

    output_data["download_hooks"] = [] if download_hooks is None else download_hooks

    output_data["source_url_metadata"] = get_url_metadata(url)

    output_data["episode_data"] = get_individual_episode_links(
        url,
        output_data["source_url_metadata"]["source_url_type"],
        after_date=after_date
    )

    return output_data


def get_individual_episode_links(source_url, source_url_type, after_date=datetime(1970, 1, 1)):
    """
    From a given link get all metadata related to the episodes
    :param source_url: bbc url
    :param source_url_type: SourceUrlType
    :param after_date: minimum first broadcast dates of episodes
    :return: list of episode metadata
    """
    after_date = pytz.utc.localize(after_date)

    def get_episode_data(episode_url):
        data = get_url_metadata(episode_url)
        data["episode_url"] = episode_url
        data["after_date"] = (
                after_date - timedelta(seconds=data["playlist_metadata"]["duration"])
                <= data["show_metadata"]["first_broadcast_date"]
        )

        return data

    sanitised_link = source_url[:-1] if source_url.endswith("/") else source_url
    sanitised_link = f"{sanitised_link}/episodes/player" if source_url_type == SourceUrlType.SHOW else sanitised_link

    if source_url_type == SourceUrlType.EPISODE:
        episode_data = get_episode_data(source_url)
        return [episode_data] if episode_data["after_date"] else []

    all_urls = extract_bbc_links(sanitised_link)

    all_urls_with_metadata = [
        get_episode_data(url)
        for url in all_urls
    ]

    all_urls_after_date = [
        url
        for url in all_urls_with_metadata
        if url["after_date"]
    ]

    return all_urls_after_date


def get_url_metadata(source_url):
    """
    Get metadata for a url
    :param source_url: bbc url
    :return: metadata
    """
    def get_metadata(get_func, url):
        try:
            return get_func(url)
        except JSONDecodeError:
            return None

    playlist_metadata = get_metadata(get_show_playlist_data, source_url)
    show_metadata = get_metadata(get_show_metadata, source_url)

    return {
        "playlist_metadata": playlist_metadata,
        "show_metadata": show_metadata,
        "source_url_type": SourceUrlType.url_to_enum(source_url, show_metadata)
    }


if __name__ == '__main__':
    download_data_extractor("https://www.bbc.co.uk/programmes/b01dmw90/episodes/player", "./", True, [],
                            datetime(1970, 1, 1))
    download_data_extractor("https://www.bbc.co.uk/programmes/b01dmw90", "./", True, [], datetime(1970, 1, 1))
    download_data_extractor("https://www.bbc.co.uk/programmes/m00082n0", "./", True, [], datetime(1970, 1, 1))
