import re
import time
from typing import List, Dict, Union
from bs4 import BeautifulSoup
import requests
from tqdm.auto import tqdm, trange


class ArcaScrapper:
    def __init__(self, parser: str = "html.parser"):
        self.ARCA_URL = "https://arca.live"
        self.parser = parser

    def get_page_contents_start_to_end(
        self,
        channel: str,
        start: int,
        end: int,
        isbest: bool = False,
        category: str = None,
    ) -> List[dict]:
        "start 페이지부터 end 페이지까지의 정보를 크롤링하는 함수"
        data = []

        for page in trange(start, end + 1, desc="page"):
            urls = self.get_post_urls(channel, page, isbest, category)

            for post_url in tqdm(urls, desc="post", leave=False):
                data.append(self.get_post_contents(post_url))
                time.sleep(0.1)

            time.sleep(0.1)

        return data

    def get_post_urls(
        self,
        channel: str,
        page_num: int,
        isbest: bool = False,
        category: str = None,
    ) -> List[str]:
        "페이지에 있는 게시물들의 url들을 담은 리스트를 반환하는 함수"
        params = {"p": page_num}
        if isbest:
            params["mode"] = "best"
        if category is not None:
            params["category"] = category

        response = requests.get(f"{self.ARCA_URL}/b/{channel}", params=params)
        soup = BeautifulSoup(response.text, self.parser)
        table = soup.find("div", class_="list-table")

        post_urls = []

        for a in table.find_all("a", href=True):
            if a["class"] == ["vrow"]:
                post_urls.append(a["href"])

        return post_urls

    def get_comment_page_nums(self, post_url: str) -> int:
        "해당 게시물의 댓글 페이지가 총 몇 페이지인지를 찾아 그 값을 반환하는 함수"
        url = self.ARCA_URL + post_url

        response = requests.get(url)
        soup = BeautifulSoup(response.text, self.parser)

        comments_box = soup.find("div", id="comment")
        page_num = comments_box.find_all("a", class_="page-link")
        return len(page_num) - 1 if page_num else 1

    def get_post_id(self, post_url: str) -> int:
        "get_post_urls로 찾아낸 url에서 id만 찾아 반환하는 함수"
        post_id = re.match(r"^/b/\w+/(\d+)\?.+$", post_url)
        return int(post_id.group(1))

    def get_post_contents(self, post_url: str) -> Dict[str, Union[int, str, List[str]]]:
        "해당 게시물의 제목과 본문, 댓글들을 찾아 반환하는 함수"
        url = self.ARCA_URL + post_url
        page_num = self.get_comment_page_nums(post_url)

        response = requests.get(url)
        soup = BeautifulSoup(response.text, self.parser)

        # 제목, 카테고리
        article_head = soup.find("div", class_="article-head")
        title_texts = article_head.find("div", class_="title").find_all(text=True)
        title = title_texts[-1].strip()
        category = title_texts[-2].strip()

        # 작성 시간
        utc_time_str = article_head.find("time").get_text(strip=True)
        utc_time = time.strptime(utc_time_str, "%Y-%m-%d %H:%M:%S")
        ts = time.mktime(utc_time) + 32400
        kst_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(ts))

        # 본문
        article_content = soup.find("div", class_="fr-view article-content")
        contents = []
        for p in article_content.find_all("p"):
            contents.append(p.text)
        contents = "\n".join(contents).replace("\xa0", " ").strip()

        # 댓글
        comments = []
        for page in range(1, page_num + 1):
            comments += self.get_post_comments(post_url, page)

        return {
            "id": self.get_post_id(post_url),
            "title": title,
            "category": category,
            "time": kst_time,
            "contents": contents,
            "comments": comments,
        }

    def get_post_comments(self, post_url: str, page_num: int = 1) -> List[str]:
        "해당 게시물의 'page_num'페이지의 댓글을 담아 반환하는 함수"
        url = self.ARCA_URL + post_url
        params = {"cp": page_num}

        response = requests.get(url, params=params)
        soup = BeautifulSoup(response.text, self.parser)

        comments_box = soup.find("div", id="comment")
        comments = []

        for reply in comments_box.find_all("div", class_="text"):
            text = reply.text.replace("\n", " ").strip()
            if text:
                comments.append(text)

        return comments
