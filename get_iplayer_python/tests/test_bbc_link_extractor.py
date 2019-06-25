import unittest

from get_iplayer_python.bbc_link_extractor import extract_bbc_links


def fake_html_getter(html: str):
    def name(url: str):
        return html
    return name


class TestBbcLinkExtractor(unittest.TestCase):
    iplayer_html = """
    <a href="https://www.bbc.co.uk/programmes/m0005zsn" class="br-blocklink__link block-link__target" data-linktrack="programmeobjectlink=title"><span class="programme__title gamma"><span>Diplo in the mix</span></span></a>
    <a>previous</a>
    <a href="https://www.youtube.com"></a>
    """

    def test_if_can_extract_iplayer_links(self):
        expected = ["https://www.bbc.co.uk/programmes/m0005zsn"]
        link = "https://www.bbc.co.uk/programmes/b01dmw90/episodes/player"
        actual = extract_bbc_links(link, fake_html_getter(self.iplayer_html))
        self.assertEqual(expected, actual)
