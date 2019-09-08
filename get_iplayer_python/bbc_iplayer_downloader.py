import logging
import os
import string
from datetime import datetime
from pathlib import Path

from get_iplayer_python.bbc_dash_xml_extractor import get_stream_selection_xml
from get_iplayer_python.downloader.downloader import download
from get_iplayer_python.ffmpeg_wrapper import merge_audio_and_video, save_audio
from get_iplayer_python.models.Exceptions import BbcException
from get_iplayer_python.mpd_data_extractor import get_stream_selection_links, create_templates
from get_iplayer_python.extractors.download_data_extractor import download_data_extractor


def download_from_url(url,
                      location,
                      overwrite=False,
                      audio_only=False,
                      download_hooks=None,
                      after_date=datetime(1970, 1, 1),
                      output_format=None,
                      logger=logging.getLogger(__name__)):
    def update_download_hook(hooks, info_dict: dict):
        for hook in hooks:
            hook(info_dict)

    def download_show(show_location, playlist_info):
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
            for format_template in templates:
                if not any([f for f in all_formats if f["mimetype"] == format_template["mimetype"]]):
                    all_formats.append({"mimetype": format_template["mimetype"], "templates": []})
                for mime_types in all_formats:
                    if mime_types["mimetype"] == format_template["mimetype"]:
                        mime_types["templates"].append(format_template)

            best_formats = {}
            for sort_format in all_formats:
                best_format = sorted(sort_format["templates"], key=int_key("bandwidth"), reverse=True)[0]
                media_type = best_format["mimetype"].split("/")[0]
                best_formats[media_type] = {
                    "template": best_format,
                    "media_type": media_type,
                    "extension": "m4a" if media_type == "audio" else best_format["mimetype"].split("/")[1]
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

        def get_output_filename(file, output_title, pid, extension=None):
            valid_chars = "-_.()%s%s" % (string.ascii_letters, string.digits)
            output_title = ''.join(c if c in valid_chars else '_' for c in output_title)
            output_title = f"{output_title}-{pid}"
            ext = extension if extension is not None else file["extension"]
            return "%s%s.%s" % (
                file["location"], output_title, ext)

        def merge_video_and_audio_files(audio_file, video_file, pid, output_title):
            audio_file_location = get_file_name(audio_file)
            video_file_location = get_file_name(video_file)
            output_title_location = get_output_filename(video_file, output_title, pid)
            merge_audio_and_video(audio_file_location, video_file_location, output_title_location)

        def save_audio_files(audio_file, pid, output_title):
            audio_file_location = get_file_name(audio_file)
            output_title_location = get_output_filename(audio_file, output_title, pid, "m4a")
            save_audio(audio_file_location, output_title_location)

        def cleanup(downloaded_formats):
            for _, value in downloaded_formats.items():
                downloaded_path = get_file_name(value)
                if Path(downloaded_path).exists():
                    os.remove(downloaded_path)

        # stream setup
        stream_selection_xml = get_stream_selection_xml(playlist_info["vpid"])
        stream_selection_links = get_stream_selection_links(stream_selection_xml.content)

        # template generation
        # get highest priority mpeg dash link with highest bit rate
        top_mpeg_dash = sorted(stream_selection_links, key=two_keys("priority", "bitrate"), reverse=True)[0]
        # get highest bandwidth download template
        formats = get_best_templates_for_mimetypes(top_mpeg_dash["href"])

        if audio_only:
            formats = {"audio": formats["audio"]}

        if not any(formats):
            logger.error("not available formats to download")
            return

        media_type_keys = list(formats.keys())

        formats[media_type_keys[0]]["location"] = show_location
        final_file_name = get_output_filename(
            formats[media_type_keys[0]],
            playlist_info["title"],
            playlist_info["vpid"]
        )
        path_filename = Path(final_file_name)
        if path_filename.is_file() and not overwrite:
            logging.warning(f"{final_file_name} already exists skipping...")
            return

        for media_type_value, template in formats.items():
            template["location"] = show_location
            template["download_filename"] = "%s-%s" % (playlist_info["title"], media_type_value)
            download_template(template)

        if "audio" in media_type_keys and "video" in media_type_keys:
            merge_video_and_audio_files(
                formats["audio"],
                formats["video"],
                playlist_info["vpid"],
                playlist_info["title"]
            )

        if len(media_type_keys) == 1 and "audio" in media_type_keys:
            save_audio_files(
                formats["audio"],
                playlist_info["vpid"],
                playlist_info["title"]
            )

        cleanup(formats)

        return get_output_filename(formats[media_type_keys[0]], playlist_info["title"], playlist_info["vpid"])

    download_hooks = [] if download_hooks is None else download_hooks

    try:
        download_data = download_data_extractor(url, location, audio_only, download_hooks, after_date)
    except BbcException as e:
        logger.exception(e)
        return

    

    for link in links:
        update_download_hook(download_hooks, {
            "status": "downloading"
        })
        file_name = download_show(location, links_playlist_info[link])
        update_download_hook(download_hooks, {
            "status": "finished",
            "filename": file_name
        })
    logger.info(f"download of playlist {title} to {location} complete")


if __name__ == '__main__':
    download_from_url("https://www.bbc.co.uk/programmes/b01dmw90/episodes/player", "./")
