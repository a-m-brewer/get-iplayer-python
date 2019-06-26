import logging
import re

from get_iplayer_python.bbc_dash_xml_extractor import get_stream_selection_xml
from get_iplayer_python.bbc_link_extractor import extract_bbc_links
from get_iplayer_python.bbc_metadata_generator import get_show_playlist_data, get_show_metadata
from get_iplayer_python.downloader.downloader import download
from get_iplayer_python.mpd_data_extractor import get_stream_selection_links, create_templates
from get_iplayer_python.url_validator import is_programme_page, is_episode_page, is_bbc_url, is_playlist_page


def download_from_url(url, location):
    def download_show(show_url, show_location):
        # helpers
        def two_keys(a, b):
            def _k(item):
                return item[a], item[b]
            return _k

        def int_key(a):
            def _k(item):
                return int(item[a])
            return _k

        # information
        playlist_info = get_show_playlist_data(show_url)
        show_info = get_show_metadata(show_url)
        show_title = show_info["display_title"]

        logger.info("downloading %s - %s" % (show_title["subtitle"], show_title["title"]))

        # stream setup
        stream_selection_xml = get_stream_selection_xml(playlist_info["vpid"])
        stream_selection_links = get_stream_selection_links(stream_selection_xml.content)

        # template generation
        # get highest priority mpeg dash link with highest bit rate
        top_mpeg_dash = sorted(stream_selection_links, key=two_keys("priority", "bitrate"), reverse=True)[0]
        # get highest bandwidth download template
        highest_bandwidth_template = sorted(create_templates(top_mpeg_dash["href"]),
                                            key=int_key("bandwidth"), reverse=True)[0]

        # download show
        download("%s%s-%s" % (show_location, show_title["subtitle"], show_title["title"]), "m4a", highest_bandwidth_template)
        logger.info("downloaded %s - %s" % (show_title["subtitle"], show_title["title"]))

    def prepare_links(links_url: str):
        sanitized_url = links_url
        is_episode = is_episode_page(links_url)
        if links_url.endswith("/"):
            links_url = links_url[:-1]
        if is_episode:
            return is_episode, sanitized_url, [links_url]
        if is_programme_page(links_url):
            links_url += "/episodes/player"
        if is_playlist_page(links_url):
            sanitized_url = re.sub("/episodes/player$", "", sanitized_url)

        return is_episode, sanitized_url, extract_bbc_links(links_url)

    if not is_bbc_url(url):
        logging.error(f"not a bbc url: {url}")
        return

    logger = logging.getLogger(__name__)

    episode_url, checked_url, links = prepare_links(url)

    show_metadata = get_show_metadata(checked_url)

    title = show_metadata["display_title"]["subtitle"] if episode_url else show_metadata["display_title"]["title"]

    logging.info(f"downloading {'episode' if episode_url else 'playlist'}")

    logger.info(f"staring download of  {title} to {location}")
    for link in links:
        download_show(link, location)
    logger.info(f"download of playlist {title} to {location} complete")
