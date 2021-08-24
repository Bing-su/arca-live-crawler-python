import argparse
from datetime import datetime
import json
import os
import time

from tqdm.auto import tqdm, trange

from arca_scrapper import ArcaScrapper


# argparse 설정
parser = argparse.ArgumentParser()
parser.add_argument("channel", type=str, help="아카라이브의 채널명(영어)")
parser.add_argument("start", type=int, help="크롤링을 시작할 페이지 번호")
parser.add_argument("end", type=int, help="크롤링을 끝낼 페이지 번호")
parser.add_argument(
    "-b", "--best", action="store_true", help="이 옵션을 사용하면 개념글에서 페이지를 크롤링합니다."
)
parser.add_argument("-c", "--category", type=str, help="크롤링할 카테고리 이름")
parser.add_argument("-n", "--file_name", type=str, help="결과물 파일의 이름")
parser.add_argument("-s", "--save_path", type=str, help="결과물 파일을 저장할 경로")
parser.add_argument(
    "-p",
    "--parser",
    type=str,
    default="html.parser",
    help='사용할 파서의 종류, 기본값="html.parser"',
)
parser.add_argument(
    "-w", "--workers", type=int, help="ThreadPoolExecutor가 사용할 max_workers 수"
)

args = parser.parse_args()

# 파일 이름 정하기
if args.file_name is None:
    t = datetime.now()
    now = f"{t.year % 100}{t.month:02}{t.day:02}-{t.hour:02}{t.minute:02}{t.second:02}"
    file_name = f"{args.channel}_{now}.json"
else:
    file_name = args.file_name
    if not file_name.endswith(".json"):
        file_name += ".json"

# 저장 경로 정하기
if args.save_path is None:
    if not os.path.isdir("data"):
        os.mkdir("data")
    save_path = ".\\data"
else:
    save_path = args.save_path


now = datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S")

# 크롤링 시작
arca = ArcaScrapper(args.parser, args.workers)
data = arca.get_page_contents_start_to_end(
    args.channel, args.start, args.end, args.best, args.category
)

total_data = len(data)
total_comments = sum(len(d["comments"]) for d in data)
json_data = {
    "channel": args.channel,
    "category": args.category if args.category is not None else "전체",
    "best_only": args.best,
    "start_page": args.start,
    "end_page": args.end,
    "scrapped_time": now,
    "total_data": total_data,
    "total_comments": total_comments,
    "data": data,
}

# 파일 저장
with open(os.path.join(save_path, file_name), "w", encoding="utf-8") as file:
    json.dump(json_data, file, ensure_ascii=False, indent=4)
    print(f"파일 저장: {os.path.join(save_path, file_name)}")

print(f"완료, 크롤링한 게시물 수: {total_data}")
