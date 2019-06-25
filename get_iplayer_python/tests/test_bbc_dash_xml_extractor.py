import unittest

from get_iplayer_python.bbc_dash_xml_extractor import random_of_set_length


def fake_xml_getter(xml):
    def name(url: str):
        return xml
    return name


class TestBbcDashXmlExtractor(unittest.TestCase):

    def test_can_get_random_5_long_number(self):
        expected = 5
        actual = random_of_set_length(5)
        self.assertEqual(expected, len(str(actual)))
