import requests as rq
from collections import deque

from typing import List
from bs4 import BeautifulSoup


API = "https://ru.wikipedia.org"


def get_link(url):
    resp = rq.get(url)
    if resp.status_code != 200:
        print("Can't fetch data!")
        exit(0)
    soup = BeautifulSoup(resp.content, "html5lib")

    urls = []
    soup = soup.find("div", {"id": "content"})
    for links in soup.find_all("a"):
        link = str(links.get("href"))
        if link.startswith("/wiki/"):
            main = API + link
            urls.append(main)
    return urls


def bfs(start, end):
    visited = set()
    if start == end:
        return start
    queue = deque([(start, [start])])
    while queue:
        url, path = queue.popleft()
        if url == end:
            return path
        if url in visited:
            continue
        visited.add(url)
        for link in get_link(url):
            if link not in visited:
                queue.append((link, path + [link]))
        if len(queue) == 0:
            return None


def find_paragraph(src, url):
    resp = rq.get(src)
    if resp.status_code != 200:
        print("Can't fetch data!")
        exit(0)
    # finding all div with content 'id'
    soup = BeautifulSoup(resp.content, "html.parser")
    texts = []
    paragraphs = soup.find_all("p")
    for x in paragraphs:
        for p in x.find_all("a"):
            our_url = p.get("href")
            if API + our_url == url:
                texts.append(x.get_text() + f" {url}")
    return texts


def main():
    URL1 = str(
        input(
            "Type src url, remember, that I work only 'https://ru.wikipedia.org' type of URL's: \n"
        )
    )
    URL2 = str(input("Type destination url: \n"))
    all_urls = bfs(URL1, URL2)
    if all_urls is not None:
        if len(all_urls) == 1:
            print("Something wrong, maybe your destination and src same links")
        # from all_urls we got list of urls, for example [url1, url2, url3]
        # it is mean, there are url2 in somewhere in url1, and so one, so one
        # we can say that, there are n url(site) in n-1 site
        if len(all_urls) == 2:
            src, dest = all_urls[0], all_urls[-1]
            text = find_paragraph(src, dest)
            print(text[0])
        if len(all_urls) > 2:
            for x in range(1, len(all_urls) - 1):
                src, dest = all_urls[x - 1], all_urls[x]
                text = find_paragraph(src, dest)
                for t in text:
                    print(t)


main()
