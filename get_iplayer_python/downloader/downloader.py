import logging
from pathlib import Path

import requests


def dash_downloader(filename_with_path,
                    base_dash_path,
                    initialisation_template_url,
                    download_segments,
                    overwrite,
                    logger=logging.getLogger(__name__)):
    # +1 because init segment
    total_segments = len(download_segments) + 1
    downloaded_segments = 0

    if Path(filename_with_path).is_file() and not overwrite:
        logging.warning(f"{filename_with_path} already exists skipping...")
        return

    logger.debug(f"downloading file to {filename_with_path}")

    with open(filename_with_path, "wb") as file:

        def get_message():
            return f"download {round((downloaded_segments / total_segments) * 100, 2)}% complete"

        def get_and_write_chunk(filename):
            full_url = f"{base_dash_path}{filename}"
            res = requests.get(full_url)
            file.write(res.content)

        # download init chunk
        get_and_write_chunk(initialisation_template_url)
        downloaded_segments += 1
        logger.debug(get_message())

        for chunk in download_segments:
            get_and_write_chunk(chunk["path"])
            downloaded_segments += 1
            logger.debug(get_message())

    logging.info(f"download complete {filename_with_path}")
