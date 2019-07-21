from datetime import datetime

import pytz
import requests
from bs4 import BeautifulSoup

from get_iplayer_python.bbc_metadata_generator import get_show_metadata
from get_iplayer_python.url_validator import is_programmes_url, is_episode_page, is_programme_page


def requests_website_retriever(website):
    return requests.get(website)


def extract_bbc_links(url: str, html_retriever_function=requests_website_retriever):
    results = []
    page = 1
    html = html_retriever_function(f"{url}?page={page}")
    while html.status_code != 404:
        soup = BeautifulSoup(html.text, "html.parser")
        results.extend([episode for episode in soup.findAll("div") if "data-pid" in episode.attrs])
        page += 1
        html = html_retriever_function(f"{url}?page={page}")

    links = []
    for result in results:
        links.extend([a.attrs["href"] for a in result.find_all('a', href=True) if is_programmes_url(a.attrs["href"])])

    return links


def prepare_links(links_url: str, after_date: datetime = datetime.min):
    after_date = pytz.utc.localize(after_date)
    if links_url.endswith("/"):
        links_url = links_url[:-1]
    is_episode = is_episode_page(links_url)
    is_programme = is_programme_page(links_url)
    if is_episode:
        meta = get_show_metadata(links_url)
        show_link = [] if meta["first_broadcast_date"] < after_date else [links_url]
        return is_episode, show_link
    if is_programme:
        links_url += "/episodes/player"
    after_links = [
        link for link in extract_bbc_links(links_url)
        if after_date <= get_show_metadata(link)["first_broadcast_date"]
    ]
    return is_episode, after_links


if __name__ == '__main__':
    result = prepare_links("https://www.bbc.co.uk/programmes/b01dmw90/episodes/player", datetime(2019, 7, 15))
    print(result)
