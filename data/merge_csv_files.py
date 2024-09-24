import pandas as pd
import os

# 파일이 저장된 디렉토리 경로
#directory = 'data\preprocessed\숙박'
directory = 'data\preprocessed\여행지'

# 빈 데이터프레임 리스트
df_list = []

# 디렉토리에서 모든 CSV 파일을 읽어오기
for filename in os.listdir(directory):
    if filename.endswith(".csv"):
        filepath = os.path.join(directory, filename)
        df = pd.read_csv(filepath)
        df_list.append(df)

# 모든 CSV 파일을 하나의 데이터프레임으로 합치기
merged_df = pd.concat(df_list, ignore_index=True)

# 결과를 새로운 CSV 파일로 저장
merged_df.to_csv('data\preprocessed\df_total.csv', index=False)

print("파일 병합이 완료되었습니다.")
