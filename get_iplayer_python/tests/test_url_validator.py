import unittest

from get_iplayer_python.url_validator import is_bbc_url


class UrlValidatorTests(unittest.TestCase):
    def test_if_returns_false_for_not_url(self):
        expected = False
        actual = is_bbc_url("not a url")
        self.assertEqual(expected, actual)

    def test_if_returns_true_for_bbc_url(self):
        expected = True
        actual = is_bbc_url("https://www.bbc.co.uk/programmes/b01dmw90")
        self.assertEqual(expected, actual)

    def test_returns_false_if_url_does_not_contain_pid(self):
        expected = False
        actual = is_bbc_url("https://www.bbc.co.uk/programmes")
        self.assertEqual(expected, actual)

    def test_returns_false_if_not_bbc_url(self):
        expected = False
        actual = is_bbc_url("https://www.youtube.com/programmes/b01dmw90")
        self.assertEqual(expected, actual)
