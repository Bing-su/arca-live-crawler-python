import argparse
import csv
from datetime import datetime
import os
import random
import time

from tqdm.auto import tqdm, trange

from functions import get_post_urls, get_contents


parser = argparse.ArgumentParser()
parser.add_argument("channel", type=str, help="아카라이브의 채널명(영어)")
parser.add_argument("start", type=int, help="크롤링을 시작할 페이지 번호")
parser.add_argument("end", type=int, help="크롤링을 끝낼 페이지 번호")
parser.add_argument(
    "-b", "--best", action="store_true", help="이 옵션을 사용하면 개념글에서 페이지를 크롤링합니다."
)
parser.add_argument("-n", "--file_name", type=str, help="결과물 파일의 이름")
parser.add_argument("-p", "--path", type=str, help="결과물 파일을 저장할 경로")

args = parser.parse_args()

# 파일 이름 정하기
if args.file_name is None:
    t = datetime.now()
    now = f"{t.year % 100}{t.month:02}{t.day:02}-{t.hour:02}{t.minute:02}{t.second:02}"
    file_name = f"{args.channel}_{now}.csv"
else:
    file_name = args.file_name + ".csv"

# 저장 경로 정하기
if args.path is None:
    if not os.path.isdir("data"):
        os.mkdir("data")
    path = "./data"
else:
    path = args.path


file = open(os.path.join(path, file_name), "w", encoding="utf-8", newline="")
writer = csv.writer(file)
writer.writerow(["content", "label"])

# 크롤링 시작
comments_count = 0
for page in trange(args.start, args.end + 1, desc="page"):
    urls = get_post_urls(args.channel, page, args.best)

    for url in tqdm(urls, desc="post", leave=False):
        contents = get_contents(url)

        title = contents["title"]
        content = contents["content"]
        comments = contents["comments"]

        for comment in comments:
            writer.writerow([comment, 0])
            comments_count += 1

    time.sleep(0.423 + random.random())

file.close()
print(f"완료, 크롤링한 댓글 수: {comments_count}")
