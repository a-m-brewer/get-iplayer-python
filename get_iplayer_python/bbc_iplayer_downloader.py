from get_iplayer_python.bbc_dash_xml_extractor import get_stream_selection_xml
from get_iplayer_python.bbc_link_extractor import extract_bbc_links
from get_iplayer_python.bbc_metadata_generator import get_show_playlist_data, get_show_metadata
from get_iplayer_python.downloader.downloader import download
from get_iplayer_python.mpd_data_extractor import get_stream_selection_links, create_templates


def download_from_url(url, location):
    def download_show(show_url, location):
        # helpers
        two_keys = lambda a, b: lambda i: (i[a], i[b])
        int_key = lambda a: lambda i: int(i[a])

        # information
        playlist_info = get_show_playlist_data(show_url)
        show_info = get_show_metadata(show_url)

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
        show_title = show_info["display_title"]
        download("%s%s-%s.m4a" % (location, show_title["subtitle"], show_title["title"]), highest_bandwidth_template)

    links = extract_bbc_links(url)

    for link in links:
        download_show(link, location)


if __name__ == '__main__':
    download_from_url("https://www.bbc.co.uk/programmes/b01dmw90/episodes/player", "./")
