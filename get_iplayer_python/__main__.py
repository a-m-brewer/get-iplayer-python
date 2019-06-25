from get_iplayer_python.bbc_dash_xml_extractor import get_stream_selection_xml
from get_iplayer_python.bbc_metadata_generator import get_show_playlist_data, get_show_metadata
from get_iplayer_python.downloader.downloader import download
from get_iplayer_python.mpd_data_extractor import get_stream_selection_links, create_templates


def main():
    url = "https://www.bbc.co.uk/programmes/m0005zsn"
    playlist_info = get_show_playlist_data(url)
    show_info = get_show_metadata(url)
    dash_xml_page = get_stream_selection_xml(playlist_info["vpid"])
    mpd_links_detail = get_stream_selection_links(dash_xml_page.content)

    def k(a, b):
        def _k(item):
            return (item[a], item[b])

        return _k

    def k1(a):
        def _k(item):
            return int(item[a])
        return _k

    mpd = sorted(mpd_links_detail, key=k("priority", "bitrate"), reverse=True)[0]
    template = sorted(create_templates(mpd["href"]), key=k1("bandwidth"), reverse=True)[0]

    title = show_info["display_title"]
    download("%s-%s.mp4" % (title["subtitle"], title["title"]), template)


if __name__ == '__main__':
    main()
