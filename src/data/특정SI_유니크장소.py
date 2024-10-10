import pandas as pd
import os

# CSV 파일 불러오기
current_dir = os.path.dirname(os.path.abspath(__file__))
#print("현재 스크립트가 실행 중인 디렉토리:", current_dir)

# 상대 경로를 사용하여 파일 경로 구성
path = os.path.join(current_dir, 'preprocessed', 'place', 'df_total.csv')

df = pd.read_csv(path)

# 특정 SI의 장소들 보기

si = '성남시'
filtered_df = df[df['SI'] == si]

print(filtered_df)

# 'other_column'의 유니크 값 출력
unique_values = filtered_df['itemID'].unique()

# 결과 출력
print(unique_values)

