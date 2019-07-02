import logging
import os
from pathlib import Path

from get_iplayer_python.bbc_dash_xml_extractor import get_stream_selection_xml
from get_iplayer_python.bbc_link_extractor import extract_bbc_links
from get_iplayer_python.bbc_metadata_generator import get_show_playlist_data, get_show_metadata
from get_iplayer_python.downloader.downloader import download
from get_iplayer_python.ffmpeg_wrapper import merge_audio_and_video
from get_iplayer_python.mpd_data_extractor import get_stream_selection_links, create_templates
from get_iplayer_python.url_validator import is_episode_page, is_bbc_url, is_playlist_page, is_programme_page


def download_from_url(url, location, overwrite=False, audio_only=False):
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

        def get_best_templates_for_mimetypes(href):
            templates = create_templates(href)

            all_formats = []
            for template in templates:
                if not any([f for f in all_formats if f["mimetype"] == template["mimetype"]]):
                    all_formats.append({"mimetype": template["mimetype"], "templates": []})
                for mime_types in all_formats:
                    if mime_types["mimetype"] == template["mimetype"]:
                        mime_types["templates"].append(template)

            best_formats = {}
            for sort_format in all_formats:
                best_format = sorted(sort_format["templates"], key=int_key("bandwidth"), reverse=True)[0]
                media_type = best_format["mimetype"].split("/")[0]
                best_formats[media_type] = {
                    "template": best_format,
                    "media_type": media_type,
                    "extension": best_format["mimetype"].split("/")[1]
                }

            return best_formats

        def download_template(data_template):
            logger.info("downloading %s" % data_template["download_filename"])
            download(data_template["location"],
                     data_template["download_filename"],
                     data_template["extension"],
                     data_template["template"],
                     overwrite=overwrite)
            logger.info("downloaded %s" % data_template["download_filename"])

        def get_file_name(file):
            return "%s%s.%s" % (
                file["location"], file["download_filename"], file["extension"])

        def get_output_filename(file, output_title):
            return "%s%s.%s" % (
                file["location"], output_title, file["extension"])

        def merge_video_and_audio_files(audio_file, video_file, output_title):
            audio_file_location = get_file_name(audio_file)
            video_file_location = get_file_name(video_file)
            output_title_location = get_output_filename(video_file, output_title)
            merge_audio_and_video(audio_file_location, video_file_location, output_title_location)

        def cleanup(downloaded_formats):
            for _, value in downloaded_formats.items():
                downloaded_path = get_file_name(value)
                os.remove(downloaded_path)

        # information
        playlist_info = get_show_playlist_data(show_url)

        # stream setup
        stream_selection_xml = get_stream_selection_xml(playlist_info["vpid"])
        stream_selection_links = get_stream_selection_links(stream_selection_xml.content)

        # template generation
        # get highest priority mpeg dash link with highest bit rate
        top_mpeg_dash = sorted(stream_selection_links, key=two_keys("priority", "bitrate"), reverse=True)[0]
        # get highest bandwidth download template
        formats = get_best_templates_for_mimetypes(top_mpeg_dash["href"])

        if not any(formats):
            logger.error("not available formats to download")
            return

        media_type_keys = list(formats.keys())

        formats[media_type_keys[0]]["location"] = show_location
        final_file_name = get_output_filename(formats[media_type_keys[0]], playlist_info["title"])
        path_filename = Path(final_file_name)
        if path_filename.is_file() and not overwrite:
            logging.warning(f"{final_file_name} already exists skipping...")
            return

        for media_type_value, template in formats.items():
            template["location"] = show_location
            template["download_filename"] = "%s-%s" % (playlist_info["title"], media_type_value)
            download_template(template)

        if "audio" in media_type_keys and "video" in media_type_keys:
            merge_video_and_audio_files(formats["audio"], formats["video"], playlist_info["title"])

        if len(media_type_keys) == 1:
            downloaded_f = formats[media_type_keys[0]]
            downloaded_format_name = get_file_name(downloaded_f)
            output_f = get_output_filename(downloaded_f, playlist_info["title"])
            os.rename(downloaded_format_name, output_f)

        cleanup(formats)

    def prepare_links(links_url: str):
        if links_url.endswith("/"):
            links_url = links_url[:-1]
        is_episode = is_episode_page(links_url)
        is_programme = is_programme_page(links_url)
        if is_episode:
            return is_episode, [links_url]
        if is_programme:
            links_url += "/episodes/player"
        return is_episode, extract_bbc_links(links_url)

    if not is_bbc_url(url):
        logging.error(f"not a bbc url: {url}")
        return

    if not location.endswith("/"):
        location += "/"

    logger = logging.getLogger(__name__)

    episode_url, links = prepare_links(url)

    programme_metadata = get_show_metadata(url)

    title = programme_metadata["title"]

    logging.info(f"downloading {'episode' if episode_url else 'playlist'}")

    logger.info(f"staring download of  {title} to {location}")
    for link in links:
        download_show(link, location)
    logger.info(f"download of playlist {title} to {location} complete")
