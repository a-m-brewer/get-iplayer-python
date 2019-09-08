import string


def get_final_filename(title, subtitle, pid, extension):
    metadata_title = f"{title} - {subtitle}"
    # remove invalid characters
    metadata_title = remove_invalid_chars(metadata_title)
    # add pid just in case the title of the episode is the same e.g. Diplo in the mix
    metadata_title += f"-{pid}"
    return f"{metadata_title}.{extension}"


def get_download_item_filename(title, subtitle, filetype):
    """
    get the temporary filenames of streams e.g. audio
    :param title:
    :param subtitle:
    :param filetype:
    :return:
    """
    metadata_title = f"{title} - {subtitle}"
    metadata_title = remove_invalid_chars(metadata_title)
    metadata_title += f"-{filetype}"
    metadata_title += f".mp4"
    return metadata_title


def remove_invalid_chars(title):
    valid_chars = "-_.()%s%s" % (string.ascii_letters, string.digits)
    return ''.join(c if c in valid_chars else '_' for c in title)

