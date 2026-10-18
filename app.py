import urllib.request
import streamlit as st

# 1. 한국어 고품질 명사 데이터베이스 로드
@st.cache_data
def load_word_database():
    urls = [
        "https://raw.githubusercontent.com/insungyeo/korean-word-list/master/words.txt",
        "https://raw.githubusercontent.com/sungkim/word-relay/master/words.txt"
    ]
    online_words = set()
    for url in urls:
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=3) as response:
                lines = response.read().decode('utf-8').splitlines()
                for w in lines:
                    word = w.strip()
                    if 2 <= len(word) <= 5 and word.isalpha():
                        if not word.endswith(('하다', '되다', '이다', '받다', '스럽다')):
                            online_words.add(word)
        except Exception:
            continue

    built_in_nouns = [
        "대한민국", "백의민족", "한글날", "태극기", "애국가", "무궁화", "거북선", "첨성대", "경복궁", "훈민정음",
        "독도", "한라산", "지리산", "설악산", "석굴암", "불국사", "직지심체요절", "세종대왕", "이순신", "유관순",
        "비빔밥", "김치찌개", "삼겹살", "떡볶이", "갈비탕", "짜장면", "수제비", "칼국수", "시금치", "콩나물",
        "양파", "마늘", "대파", "생강", "당근", "무말랭이", "배추김치", "깍두기", "오이소박이", "된장찌개",
        "청국장", "순두부", "부대찌개", "돈가스", "함박스테이크", "오므라이스", "김밥", "주먹밥", "샌드위치", "토스트",
        "사과나무", "바나나", "수박", "딸기", "포도", "복숭아", "오렌지", "토마토", "감자", "고구마",
        "옥수수", "단호박", "해바라기", "개나리", "진달래", "단풍잎", "무궁화", "코스모스", "선인장", "수국",
        "도서관", "박물관", "체육관", "수영장", "영화관", "백화점", "우체국", "경찰서", "소방서", "주민센터",
        "동물원", "식물원", "수족관", "놀이동산", "시청", "구청", "도청", "은행", "병원", "약국", "미용실",
        "컴퓨터", "스마트폰", "텔레비전", "냉장고", "세탁기", "청소기", "노트북", "키보드", "모니터", "안경",
        "가방", "지갑", "시계", "전화기", "선풍기", "에어컨", "전자레인지", "식기세척기", "보조배터리", "이어폰",
        "은하수", "인공지능", "우주선", "호랑이", "돌고래", "독수리", "북극곰", "다람쥐", "청상아리", "장수풍뎅이",
        "눈사람", "무지개", "태양계", "인공위성", "망원경", "현미경", "온도계", "나침반", "지구본", "지도"
    ]

    all_words = set(built_in_nouns)
    all_words.update(online_words)
    return list(all_words)

word_database = load_word_database()

# 2. 100% 자동 생성을 보장하는 가로 단어 검색 및 자동 생성 함수
def find_all_valid_words_for_char(target_char, target_word, target_col=2, max_cols=5):
    candidates = []
    
    # 1차: 사전 내 5칸 격자에 완벽히 들어맞는 명사 검색
    for word in word_database:
        if word == target_word:
            continue
            
        for char_pos, c in enumerate(word):
            if c == target_char:
                start_col = target_col - char_pos
                end_col = start_col + len(word)
                if 0 <= start_col and end_col <= max_cols:
                    candidates.append(word)
                    break
                    
    # 2차: 사전 검색 결과가 없는 희귀 글자인 경우 100% 자동 명사 조합 생성
    if not candidates:
        prefixes = ["대", "신", "초", "성", "민", "한국", "세계", "국민", "자연", "문화", "명", "청", "광", "상"]
        suffixes = ["관", "장", "회", "소", "원", "센터", "거리", "공원", "마을", "시티", "방", "점", "가", "교"]
        
        for p in prefixes:
            w = p + target_char
            if len(w) <= 4 and w != target_word:
                candidates.append(w)
        for s in suffixes:
            w = target_char + s
            if len(w) <= 4 and w != target_word:
                candidates.append(w)
        for p in ["신", "대", "초", "성"]:
            for s in ["관", "장", "원", "소"]:
                w = p + target_char + s
                if len(w) <= 5 and w != target_word:
                    candidates.append(w)

    # 글자 수 순서(2자->3자->4자->5자) 정렬 후 가나다순 정렬
    sorted_candidates = sorted(list(set(candidates)), key=lambda x: (len(x), x))
    return sorted_candidates

# 3. 페이지 레이아웃 및 디자인 설정
st.set_page_config(page_title="100% 자동 낱말퀴즈 생성기", layout="centered")

st.markdown("""
    <style>
    .quiz-container {
        display: flex;
        justify-content: center;
        margin-top: 20px;
        margin-bottom: 30px;
    }
    .quiz-grid {
        display: grid;
        grid-template-columns: repeat(5, 70px);
        grid-gap: 2px;
        background-color: #333333;
        border: 3px solid #333333;
        padding: 2px;
    }
    .grid-cell {
        width: 70px;
        height: 70px;
        background-color: #FFFFFF;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 28px;
        font-weight: bold;
        color: #000000;
        box-sizing: border-box;
        font-family: 'Malgun Gothic', 'Noto Sans KR', sans-serif;
    }
    .grid-cell.highlight-border {
        background-color: #FFE600;
        border: 3px solid #FF0000;
    }
    .grid-cell.empty {
        background-color: #EFEFEF;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🧩 100% 자동 낱말퀴즈 생성기")

# 4. 사이드바 - 정답 입력 및 100% 드롭다운 선택
st.sidebar.header("🎯 정답 단어 입력")
target_word = st.sidebar.text_input("세로 정답 단어 입력", value="대한민국")

st.sidebar.subheader("🤖 100% 자동 생성 가로 단어")
row_words = []

for i, char in enumerate(target_word):
    candidates = find_all_valid_words_for_char(char, target_word)
    # 직접 입력창 없이 100% selectbox만으로 단어 제공
    selected_word = st.sidebar.selectbox(
        f"'{char}' 포함 추천 목록 ({len(candidates)}개)", 
        options=candidates,
        key=f"select_{i}_{char}_{target_word}"
    )
    row_words.append(selected_word)

# 5. 격자 배치 계산
grid_cols = 5
target_col = 2
grid_rows = len(target_word)

grid = [["" for _ in range(grid_cols)] for _ in range(grid_rows)]

for r_idx, (target_char, h_word) in enumerate(zip(target_word, row_words)):
    if not h_word:
        continue
    
    char_pos = h_word.find(target_char)
    if char_pos != -1:
        start_col = target_col - char_pos
        for i, c in enumerate(h_word):
            c_pos = start_col + i
            if 0 <= c_pos < grid_cols:
                grid[r_idx][c_pos] = c

# 세로 정답열 빈칸 처리 (퀴즈 출제용)
for r_idx in range(grid_rows):
    grid[r_idx][target_col] = ""

# 6. HTML 화면 출력
html_code = '<div class="quiz-container"><div class="quiz-grid">'
for r in range(grid_rows):
    for c in range(grid_cols):
        char = grid[r][c]
        is_highlight = (c == target_col)
        
        cell_class = "grid-cell"
        if is_highlight:
            cell_class += " highlight-border"
        elif char == "":
            cell_class += " empty"
            
        html_code += f'<div class="{cell_class}">{char}</div>'
html_code += '</div></div>'

st.markdown(html_code, unsafe_allow_html=True)