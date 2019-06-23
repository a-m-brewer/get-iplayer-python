import requests
from bs4 import BeautifulSoup, SoupStrainer

from get_iplayer_python.url_validator import is_bbc_url


def urllib_website_retriever(website):
    return requests.get(website).text


def extract_bbc_links(url: str, html_retriever_function=urllib_website_retriever):
    html = html_retriever_function(url)
    result = []
    for item in BeautifulSoup(html, "html.parser", parse_only=SoupStrainer('a')):
        if item.has_attr('href') and is_bbc_url(item["href"]):
            result.append(item["href"])
    return result

# TODO: can get programme info from $url	https://www.bbc.co.uk/programmes/m0005zsn.json
# Maybe this url https://open.live.bbc.co.uk/mediaselector/5/select/version/2.0/mediaset/iptv-all/vpid/m0005zsl?cb=50625
# https://open.live.bbc.co.uk/mediaselector/5/select/version/2.0/mediaset/iptv-all/vpid/m0005zsl?cb=".( sprintf "%05.0f", 99999*rand(0) );
# media elements
# connection elements
#
