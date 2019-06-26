import requests
from bs4 import BeautifulSoup

from get_iplayer_python.url_validator import is_programmes_url


def requests_website_retriever(website):
    return requests.get(website).text


def extract_bbc_links(url: str, html_retriever_function=requests_website_retriever):
    html = html_retriever_function(url)

    soup = BeautifulSoup(html, "html.parser")

    results = [episode for episode in soup.findAll("div") if "data-pid" in episode.attrs]

    links = []
    for result in results:
        links.extend([a.attrs["href"] for a in result.find_all('a', href=True) if is_programmes_url(a.attrs["href"])])

    return links

