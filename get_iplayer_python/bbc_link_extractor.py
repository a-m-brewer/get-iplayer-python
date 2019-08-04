from datetime import datetime, timedelta

import pytz
import requests
from bs4 import BeautifulSoup

from get_iplayer_python.bbc_metadata_generator import get_show_metadata, get_show_playlist_data
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
        meta = __get_meta_dict(links_url)
        show_link = [] if __after_date(meta, after_date) else [links_url]
        return is_episode, show_link
    if is_programme:
        links_url += "/episodes/player"

    all_metadata = [
        __get_meta_dict(link)
        for link in extract_bbc_links(links_url)
    ]

    after_meta = [
        meta
        for meta in all_metadata
        if __after_date(meta, after_date)
    ]

    after_links = [
        meta["link"]
        for meta in after_meta
    ]

    return is_episode, after_links


def __after_date(meta, after_date):
    return after_date - timedelta(seconds=meta["playlist"]["duration"]) <= meta["show"]["first_broadcast_date"]


def __get_meta_dict(link):
    return {
        "show": get_show_metadata(link),
        "playlist": get_show_playlist_data(link),
        "link": link
    }

