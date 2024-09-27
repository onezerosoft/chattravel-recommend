import pandas as pd

# CSV 파일 불러오기
#df = pd.read_csv('data\preprocessed\여행지\df_total.csv')
df = pd.read_csv('data\preprocessed\숙박\df_total.csv')

# SI 변경
df.loc[df['SIDO'] == '세종특별시', 'SI'] = '세종특별시'
df.loc[df['SIDO'].isin(['부산', '부산광역시']), 'SI'] = '부산광역시'
df.loc[df['SIDO'].isin(['울산', '울산광역시']), 'SI'] = '울산광역시'
df.loc[df['SIDO'].isin(['대구', '대구광역시']), 'SI'] = '대구광역시'
df.loc[df['SIDO'].isin(['광주', '광주광역시']), 'SI'] = '광주광역시'
df.loc[df['SIDO'].isin(['대전', '대전광역시']), 'SI'] = '대전광역시'


# 'SI' 컬럼에서 '1'을 '2'로 변경
df['SI'] = df['SI'].replace('부산', '부산광역시')
df['SI'] = df['SI'].replace('울산', '울산광역시')
df['SI'] = df['SI'].replace('대구', '대구광역시')
df['SI'] = df['SI'].replace('광주', '광주광역시')
df['SI'] = df['SI'].replace('대전', '대전광역시')

df['SIDO'] = df['SIDO'].replace('부산', '부산광역시')
df['SIDO'] = df['SIDO'].replace('울산', '울산광역시')
df['SIDO'] = df['SIDO'].replace('대구', '대구광역시')
df['SIDO'] = df['SIDO'].replace('광주', '광주광역시')
df['SIDO'] = df['SIDO'].replace('대전', '대전광역시')

# 수정된 CSV 파일 저장
#df.to_csv('data\preprocessed\여행지\df_total.csv', index=False)
df.to_csv('data\preprocessed\숙박\df_total.csv', index=False)
#df.to_csv('data\preprocessed\df_test.csv', index=False)

print("CSV 파일이 성공적으로 수정되었습니다.")
