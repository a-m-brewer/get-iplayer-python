import logging
import os
from datetime import datetime
from pathlib import Path

from get_iplayer_python.downloader.downloader import dash_downloader
from get_iplayer_python.extractors.download_data_extractor import download_data_extractor
from get_iplayer_python.extractors.template_extractors import get_best_download_templates
from get_iplayer_python.ffmpeg_wrapper import merge_audio_and_video, save_audio
from get_iplayer_python.helpers.filenames import get_final_filename, get_download_item_filename
from get_iplayer_python.models.Exceptions import BbcException


def download_from_url(url,
                      location,
                      overwrite=False,
                      audio_only=False,
                      download_hooks=None,
                      after_date=datetime(1970, 1, 1),
                      output_format=None,
                      logger=logging.getLogger(__name__)):

    download_hooks = [] if download_hooks is None else download_hooks

    def update_hooks(message):
        for hook in download_hooks:
            hook(message)

    try:
        download_data = download_data_extractor(url, location, audio_only, download_hooks, after_date)
    except BbcException as e:
        logger.exception(e)
        return

    for episode in download_data["episode_data"]:
        try:
            # tell download hooks that an episode is currently being downloaded
            update_hooks({
                "status": "downloading"
            })

            # get the best available MPD xml
            episode_vpid = episode["playlist_metadata"]["vpid"]
            best_template = get_best_download_templates(episode_vpid, audio_only)

            # create final filename that both parts will be merged into
            final_filename_args = {
                "title": episode["show_metadata"]["display_title"]["title"],
                "subtitle": episode["show_metadata"]["display_title"]["subtitle"],
                "pid": episode["show_metadata"]["pid"],
                "extension": output_format if output_format is not None else "m4a" if audio_only else "mp4"
            }

            episode["final_filename"] = get_final_filename(**final_filename_args)
            episode["final_filename_with_path"] = f"{download_data['location']}{episode['final_filename']}"

            # skip if the file already exists
            if Path(episode["final_filename_with_path"]).is_file() and not overwrite:
                logging.warning(f"{episode['final_filename_with_path']} already exists skipping...")
                return

            # what to remove once download is done (e.g. when downloading a show there will be pre merge audio / video)
            episode["files_to_cleanup"] = []

            # although unlikely for BBC there could be multiple MPD Periods
            for period in best_template:
                # download each file type for that period
                for filetype, template in period.items():
                    filename = get_download_item_filename(
                        final_filename_args["title"],
                        final_filename_args["subtitle"],
                        filetype
                    )
                    full_path_filename = f"{download_data['location']}{filename}"
                    template["filename_with_path"] = full_path_filename

                    rep = template["representation"]
                    # download the template (this is the """ real """ download
                    dash_downloader(
                        filename_with_path=full_path_filename,
                        base_dash_path=rep["base_dash_path"],
                        initialisation_template_url=rep["initialisation_template_url"],
                        download_segments=rep["download_segments"],
                        overwrite=overwrite,
                        logger=logger
                    )

                    # append that file to be cleaned up as it is ffmpeged on the way out
                    episode["files_to_cleanup"].append(full_path_filename)

                # ffmpeg as audio or video
                if audio_only or (len(period.items()) == 1 and "audio" in period):
                    save_audio(period["audio"]["filename_with_path"], episode["final_filename_with_path"])
                else:
                    merge_audio_and_video(
                        period["audio"]["filename_with_path"],
                        period["video"]["filename_with_path"],
                        episode["final_filename_with_path"]
                    )

                # tell hooks download is complete
                update_hooks({
                    "status": "finished",
                    "filename": episode["final_filename_with_path"]
                })

            # remove laying around files
            for file in episode["files_to_cleanup"]:
                os.remove(file)

            logger.info(f"download of {url} to {location} complete!")
        except BbcException as e:
            logger.exception(e)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, format="[%(asctime)s][%(levelname)s]: %(message)s")
    logging.getLogger('urllib3.connectionpool').setLevel(logging.ERROR)
    logger = logging.getLogger(__name__)
    download_from_url("https://www.bbc.co.uk/iplayer/episode/b0074dpv/doctor-who-series-1-5-world-war-three", "./", logger=logger,
                      download_hooks=[lambda d: logger.info(d)], output_format="mkv")
