import pandas as pd
import os

# CSV 파일 불러오기
current_dir = os.path.dirname(os.path.abspath(__file__))
#print("현재 스크립트가 실행 중인 디렉토리:", current_dir)

# 상대 경로를 사용하여 파일 경로 구성
path = os.path.join(current_dir, 'preprocessed', 'place', 'df_total.csv')

df = pd.read_csv(path)

# 여행지 전처리 : 
# 특정 단어가 들어간 장소 삭제하기
df_filtered = df[~df['itemID'].str.contains("더블유", na=False)]

# 값 변경
#df_filtered['itemID'].replace('밀란 더 마켓','밀락 더 마켓', inplace=True)

# 수정된 CSV 파일 저장
path = os.path.join(current_dir, 'preprocessed', 'place', 'df_total.csv')
#path = os.path.join(current_dir, 'preprocessed', 'place','df_test.csv')

df_filtered.to_csv(path, index=False)

print("CSV 파일이 성공적으로 수정되었습니다.")
