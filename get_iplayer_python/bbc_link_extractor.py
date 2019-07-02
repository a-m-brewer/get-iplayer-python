import requests
from bs4 import BeautifulSoup

from get_iplayer_python.url_validator import is_programmes_url


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


if __name__ == '__main__':
    extract_bbc_links("https://www.bbc.co.uk/programmes/b01dmw90/episodes/player")