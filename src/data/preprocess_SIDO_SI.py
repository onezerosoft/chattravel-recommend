import pandas as pd

# 데이터 불러오기
df1 = pd.read_csv('data/preprocessed/여행지/df_total.csv')
df2 = pd.read_csv('data/preprocessed/숙박/df_total.csv')
dummy_df = pd.read_csv('data/style/dummy_data.csv')

# DISTRICT_MAP 정의
DISTRICT_MAP = {
    "수도권": [
        "서울시", "수원시", "성남시", "고양시", "용인시", "화성시", "안산시", "안양시",
        "부천시", "광명시", "이천시", "평택시", "김포시", "오산시", "남양주시", "파주시",
        "구리시", "양주시", "동두천시", "포천시", "시흥시", "의정부시", "안성시",
        "세종특별시", "인천광역시", "연천군"
    ],
    "경상남도": ["창원시", "진주시", "통영시", "사천시", "김해시", "밀양시", "거제시", "양산시",
                "함안군", "의령군", "창녕군", "남해군", "하동군", "산청군", "거창군", "합천군",
                "부산광역시"],
    "경상북도": ["포항시", "경주시", "김천시", "안동시", "구미시", "영천시", "상주시", "문경시",
                "예천군", "청송군", "영양군", "봉화군", "영덕군", "울진군", "울릉군", "울산광역시",
                "대구광역시"],
    "전라남도": ["목포시", "여수시", "순천시", "나주", "담양군", "장성군", "영광군", "함평군",
                "신안군", "무안군", "진도군", "완도군", "강진군", "해남군", "영암군", "순천시",
                "광주광역시", "장흥군", "보성군"],
    "전라북도": ["전주시", "익산시", "군산시", "남원시", "정읍시", "김제시", "완주군", "진안군",
                "무주군", "장수군", "임실군", "순창군", "고창군", "부안군"],
    "충청남도": ["천안시", "공주시", "보령시", "아산시", "서산시", "논산시", "계룡시", "당진시",
                "홍성군", "예산군", "태안군", "서천군", "청양군", "대전광역시"],
    "충청북도": ["청주시", "충주시", "제천시", "진천군", "음성군", "단양군", "괴산군", "증평군",
                "성과군"],
    "강원도": ["춘천시", "원주시", "강릉시", "동해시", "삼척시", "태백시", "속초시", "양양군",
              "홍천군", "횡성군", "영월군", "평창군", "정선군", "철원군", "인제군", "고성군",
              "양구군", "화천군"],
    "제주도": ["제주시", "서귀포시"],
}

# SI 구 목록
seoul_gu_list = [
    "강남구", "강북구", "강서구", "관악구", "구로구", "금천구", "노원구", "도봉구",
    "동대문구", "동작구", "마포구", "서대문구", "서초구", "성동구", "성북구", "송파구",
    "양천구", "영등포구", "용산구", "은평구", "종로구", "중구", "중랑구"
]

# SI를 업데이트하는 함수
def update_si(row):
    # SI가 서울 구 목록에 포함되어 있으면 SI를 '서울시'로 변경
    if row['SI'] in seoul_gu_list:
        return "서울시"
    
    if row['SI'] in ['인천']:
        return '인천광역시'
    
    return row['SI']  # 변경할 필요가 없을 경우 원래 SI 반환

# SIDO를 업데이트하는 함수
def update_sido(row):
    # SIDO가 '서울', '경기', '경기도'인 경우 '수도권'으로 변경
    if row['SIDO'] in ['서울', '서울시', '인천', '경기', '경기도']:
        return "수도권"
    
    # SI가 수도권에 포함되어 있다면 SIDO를 '수도권'으로 변경
    if row['SI'] in DISTRICT_MAP.get("수도권", []):
        return "수도권"
    
    # 나머지 경우에 대해 DISTRICT_MAP에서 SIDO를 찾음
    for sido, cities in DISTRICT_MAP.items():
        if row['SI'] in cities:
            return sido
    
    if row['SIDO'] in ['경남', '부산광역시']:
        return "경상남도"
    
    if row['SIDO'] in ['경북', '대구광역시']:
        return "경상북도"
    
    return ""  # 해당되는 값이 없을 경우 빈 문자열 반환

# df1과 df2의 SIDO 업데이트
for df in [df1, df2, dummy_df]:
    # SIDO 업데이트
    df['SIDO'] = df.apply(update_sido, axis=1)
    
    # SI를 DISTRICT_MAP에서 찾아서 업데이트
    df['SI'] = df.apply(lambda row: row['SI'] if row['SIDO'] == "" else row['SI'], axis=1)
    df['SI'] = df.apply(update_si, axis=1)

# 수정된 데이터프레임을 저장
df1.to_csv('data/preprocessed/여행지/updated_df_total.csv', index=False)
df2.to_csv('data/preprocessed/숙박/updated_df_total.csv', index=False)
dummy_df.to_csv('data/style/updated_dummy_data.csv', index=False)
