import time
from typing import List, Dict, Union
from bs4 import BeautifulSoup
import requests


ARCA_URL = "https://arca.live"


def get_post_urls(channel: str, page_num: int, isbest: bool) -> List[str]:
    if isbest:
        params = {"mode": "best", "p": page_num}
    else:
        params = {"p": page_num}

    response = requests.get(f"{ARCA_URL}/b/{channel}", params=params)
    soup = BeautifulSoup(response.text, "lxml")
    table = soup.find("div", class_="list-table")

    post_urls = []

    for a in table.find_all("a", href=True):
        if a["class"] == ["vrow"]:
            post_urls.append(a["href"])

    return post_urls


def get_comment_page_nums(post_url: str) -> int:
    url = ARCA_URL + post_url

    response = requests.get(url)
    soup = BeautifulSoup(response.text, "lxml")

    comment_box = soup.find("div", id="comment")
    page_num = comment_box.find_all("a", class_="page-link")
    return len(page_num) - 1 if page_num else 1


def get_contents(post_url: str) -> Dict[str, Union[str, List[str]]]:
    url = ARCA_URL + post_url
    page_num = get_comment_page_nums(post_url)

    response = requests.get(url)
    soup = BeautifulSoup(response.text, "lxml")

    article_head = soup.find("div", class_="article-head")
    title_texts = article_head.find("div", class_="title").find_all(text=True)
    title = title_texts[-1].strip()

    article_content = soup.find("div", class_="fr-view article-content")
    content = []
    for p in article_content.find_all("p"):
        content.append(p.text)

    comments = []
    for page in range(1, page_num + 1):
        comments += get_pages_comments(post_url, page)
        time.sleep(0.11)

    return {"title": title, "content": "\n".join(content), "comments": comments}


def get_pages_comments(post_url: str, page_num: int) -> List[str]:
    url = ARCA_URL + post_url
    params = {"cp": page_num}

    response = requests.get(url, params=params)
    soup = BeautifulSoup(response.text, "lxml")

    comments_box = soup.find("div", class_="list-area")
    comments = []
    for reply in comments_box.find_all("div", class_="text"):
        text = reply.text.replace("\n", " ").strip()
        if text:
            comments.append(text)

    return comments
