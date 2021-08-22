# arcalive-crawler-python

### 아카라이브에서 게시물을 크롤링하는 파이썬 프로그램입니다.

아카라이브의 특정 채널에서 페이지 단위로 내용물을 수집합니다.  
수집한 내용은 json파일로 저장되며 그 형태는 다음과 같습니다.
```
{
    "channel": str,  # 채널 이름
    "category": str,  # 카테고리 이름
    "scrapped_time": str,  # 크롤링 시작 시간, "%Y/%m/%d %H:%M:%S"
    "total_data": int,  # 수집한 게시물 수
    "total_comments": int,  # 수집한 댓글 수
    "data": List[dict] [  # 수집한 내용
        {
            "id": int,  # 게시물의 id
            "title": str,  # 게시물의 제목
            "category": str,  # 게시물이 속한 카테고리, 없으면 빈칸
            "contents": str,  # 게시물의 본문
            "comments": List[str]  # 게시물의 댓글
        },
    ]
}
```

## 사용방법

예) `python main.py genshin 1 2 -b`  
 -> 원신 채널의 개념글에서 1페이지부터 2페이지까지 크롤링한다.

</br>

`python main.py "채널 이름(영어)" "시작페이지" "끝페이지"`  
`-b, --best` (옵션) 사용하면 개념글 페이지에서 크롤링합니다.  
`-c, --category "카테고리 이름"` (옵션) 크롤링할 해당 채널의 카테고리 이름  
`-n, --file_name "파일 이름"` (옵션) 크롤링한 댓글들을 저장할 파일 이름.  
`-s, --save_path "경로"` (옵션) 파일을 저장할 경로. 기본적으로 현재 위치에 data폴더를 만들어 저장합니다.  
`-p, --parser "파서 이름"` (옵션) beautifulsoup4가 사용할 파서의 이름, 기본값="html.parser"  

## 요구사항
`requests`  
`beautifulsoup4`  
`tqdm`