import unittest

from get_iplayer_python.bbc_metadata_generator import get_show_metadata, get_show_playlist_data
from get_iplayer_python.tests.test_data import metadata_json, episode_playlist_json


def fake_json_getter(json):
    def name(url: str):
        return json
    return name


class TestBbcMetadataGenerator(unittest.TestCase):
    def setUp(self) -> None:
        self.test_link = "https://www.bbc.co.uk/programmes/m000669y"
        self.test_function = fake_json_getter(metadata_json)

    def test_can_get_show_title_from_json(self):
        expected = {
            "title": "Diplo and Friends",
            "subtitle": "distinkt in the mix"
        }
        actual = get_show_metadata(self.test_link, self.test_function)["display_title"]
        self.assertEqual(expected, actual)

    def test_can_get_episode_pid(self):
        expected = "m000669y"
        actual = get_show_metadata(self.test_link, self.test_function)["pid"]
        self.assertEqual(expected, actual)

    def test_can_get_image_pid(self):
        expected = "p07dsbjv"
        actual = get_show_metadata(self.test_link, self.test_function)["image_pid"]
        self.assertEqual(expected, actual)

    def test_can_get_vpid_from_playlist_data(self):
        expected = "m000669t"
        actual = get_show_playlist_data("test", fake_json_getter(episode_playlist_json))["vpid"]
        self.assertEqual(expected, actual)

    def test_can_get_image_url_from_playlist_data(self):
        expected = "http://ichef.bbci.co.uk/images/ic/976x549/p07f0n8q.jpg"
        actual = get_show_playlist_data("test", fake_json_getter(episode_playlist_json))["image_url"]
        self.assertEqual(expected, actual)