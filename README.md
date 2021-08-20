# arca-live-crawler-python

### 아카라이브에서 댓글을 크롤링하는 파이썬 프로그램입니다.

제목, 내용도 일단 수집하지만 사용하지는 않습니다.

## 사용방법

예) `python main.py genshin 1 2 -b`  
 -> 원신 채널의 개념글에서 1페이지부터 2페이지까지 크롤링한다.

</br>

`python main.py "채널 이름(영어)" "시작페이지" "끝페이지"`  
`-b, --best` (옵션) 사용하면 개념글 페이지에서 크롤링합니다.  
`--file_name` (옵션) 크롤링할 댓글을 저장할 파일 이름. 자동으로 뒤에 .csv가 붙습니다.  
`--path` (옵션) 파일을 저장할 경로. 기본적으로 현재 위치에 data폴더를 만들어 저장합니다.

## 요구사항
`requests`  
`beautifulsoup4`  
`lxml`  
`tqdm`