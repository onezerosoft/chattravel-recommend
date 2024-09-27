import pandas as pd
import os

# CSV 파일 불러오기
current_dir = os.path.dirname(os.path.abspath(__file__))
print("현재 스크립트가 실행 중인 디렉토리:", current_dir)

# 상대 경로를 사용하여 파일 경로 구성
#path = os.path.join(current_dir, 'preprocessed', 'place', 'df_total.csv')
path = os.path.join(current_dir, 'preprocessed', 'accomodation', 'df_total.csv')

df = pd.read_csv(path)

# SI 변경
df.loc[df['SIDO'] == '서울', 'SI'] = '서울시'
# df.loc[df['SIDO'].isin(['부산', '부산광역시']), 'SI'] = '부산광역시'
# df.loc[df['SIDO'].isin(['울산', '울산광역시']), 'SI'] = '울산광역시'
# df.loc[df['SIDO'].isin(['대구', '대구광역시']), 'SI'] = '대구광역시'
# df.loc[df['SIDO'].isin(['광주', '광주광역시']), 'SI'] = '광주광역시'
# df.loc[df['SIDO'].isin(['대전', '대전광역시']), 'SI'] = '대전광역시'


# 'SI' 컬럼에서 '1'을 '2'로 변경
# df['SI'] = df['SI'].replace('부산', '부산광역시')
# df['SI'] = df['SI'].replace('울산', '울산광역시')
# df['SI'] = df['SI'].replace('대구', '대구광역시')
# df['SI'] = df['SI'].replace('광주', '광주광역시')
# df['SI'] = df['SI'].replace('대전', '대전광역시')

df['SIDO'] = df['SIDO'].replace('경기', '경기도')
df['SIDO'] = df['SIDO'].replace('강원', '강원도')
df['SIDO'] = df['SIDO'].replace('경북', '경상북도')
df['SIDO'] = df['SIDO'].replace('경남', '경상남도')
df['SIDO'] = df['SIDO'].replace('전북', '전라북도')
df['SIDO'] = df['SIDO'].replace('충북', '충청북도')
df['SIDO'] = df['SIDO'].replace('충남', '충청남도')
df['SIDO'] = df['SIDO'].replace('제주특별자치도', '제주도')


# 수정된 CSV 파일 저장
#path = os.path.join(current_dir, 'preprocessed', 'place', 'df_total.csv')
#path = os.path.join(current_dir, 'preprocessed', 'accomodation', 'df_total.csv')
path = os.path.join(current_dir, 'preprocessed', 'df_test.csv')

print(path)
df.to_csv(path, index=False)

print("CSV 파일이 성공적으로 수정되었습니다.")
