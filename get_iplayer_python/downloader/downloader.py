import logging
import os
from pathlib import Path

import requests
from requests.adapters import HTTPAdapter
from urllib3 import Retry


def download(path, filename, extension, template, overwrite=False):
    logger = logging.getLogger(__name__)
    total_frag = len(template["fragments"]) + 1
    fragments_downloaded = 0
    temporary_filename = f"{path}{filename}.part"
    output_filename = f"{path}{filename}.{extension}"

    path_filename = Path(output_filename)
    if path_filename.is_file() and not overwrite:
        logging.warning(f"{output_filename} already exists skipping...")
        return

    def requests_retry_session(
            retries=3,
            backoff_factor=0.3,
            status_forcelist=(500, 502, 504),
            session=None) -> requests.adapters.HTTPAdapter:
        session = session or requests.Session()
        retry = Retry(
            total=retries,
            read=retries,
            connect=retries,
            backoff_factor=backoff_factor,
            status_forcelist=status_forcelist,
        )
        adapter = HTTPAdapter(max_retries=retry)
        session.mount('http://', adapter)
        session.mount('https://', adapter)
        return session

    def get_message():
        return f"download of file: {filename} is {round((fragments_downloaded / total_frag) * 100, 2)}% complete"

    with open(temporary_filename, "wb") as file:
        def get_and_write_chunk(chunk_address):
            try:
                response = requests_retry_session().get(chunk_address, stream=True)
                file.write(response.content)
            except requests.HTTPError:
                logger.exception(f"failed to download initialization chunk for {filename} url: {chunk_address}")
            except OSError:
                logger.exception(f"could not download initialization chunk for {filename}")
            finally:
                logging.debug(get_message())

        get_and_write_chunk("%s%s" % (template["base_url"], template["init_url"]))
        fragments_downloaded += 1

        for frag in template["fragments"]:
            get_and_write_chunk("%s%s" % (template["base_url"], frag["path"]))
            fragments_downloaded += 1
    os.rename(temporary_filename, output_filename)
