from enum import Enum

from get_iplayer_python.url_validator import is_episode_page, is_programme_page


class SourceUrlType(Enum):
    UNKNOWN = -1
    EPISODE = 0
    SHOW = 1,
    PLAYLIST = 2

    @staticmethod
    def url_to_enum(source_url, show_metadata):
        programme_page = is_programme_page(show_metadata, source_url)
        episode_page = is_episode_page(show_metadata)
        playlist_page = source_url.endswith("/episodes/player")

        if programme_page:
            return SourceUrlType.SHOW
        elif episode_page:
            return SourceUrlType.EPISODE
        elif playlist_page:
            return SourceUrlType.PLAYLIST
        else:
            return SourceUrlType.UNKNOWN
