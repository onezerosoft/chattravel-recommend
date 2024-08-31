import pandas as pd


def main():
  # 1. 데이터 로드
  file = r'data\TL_csv_E\tn_visit_area_info_방문지정보_E.csv'
  # file = r'data\TL_csv_F\tn_visit_area_info_방문지정보_F.csv'
  # file = r'data\TL_csv_G\tn_visit_area_info_방문지정보_G.csv'
  # file = r'data\TL_csv_H\tn_visit_area_info_방문지정보_H.csv'
  
  visit = pd.read_csv(file)
  id_list=['H']
  
  # 2. 데이터 전처리
  visit_data_list=[visit]

  for id,visit_area_info in zip(id_list,visit_data_list):
    # 관광지 선택
    visit_info = visit_area_info[ (visit_area_info['VISIT_AREA_TYPE_CD'] == 1) |
    (visit_area_info['VISIT_AREA_TYPE_CD'] == 2) |(visit_area_info['VISIT_AREA_TYPE_CD'] == 3) | (visit_area_info['VISIT_AREA_TYPE_CD'] == 4) |
      (visit_area_info['VISIT_AREA_TYPE_CD'] == 5) | (visit_area_info['VISIT_AREA_TYPE_CD'] == 6) |(visit_area_info['VISIT_AREA_TYPE_CD'] == 7) |
      (visit_area_info['VISIT_AREA_TYPE_CD'] == 8)]

    visit_info = visit_area_info[ (visit_area_info['VISIT_AREA_TYPE_CD'] == 4) ]

    visit_info = visit_info.groupby('VISIT_AREA_NM').filter(lambda x: len(x) > 1)
    visit_info=visit_info.reset_index(drop = True)

  visit_final_E=visit_info
  visit_final_E['ratings'] = visit_final_E[['DGSTFN', 'REVISIT_INTENTION', 'RCMDTN_INTENTION']].mean(axis=1)
  visit_final_E['TRAVELER_ID'] = visit_final_E['TRAVEL_ID'].str.split('_').str[1]
  
  # 3. 세부 전처리
  visit_final_E['SIDO'] = visit_final_E['LOTNO_ADDR'].str.split().str[0]
  visit_final_E['SI'] = visit_final_E['LOTNO_ADDR'].str.split().str[1]
  

  dfe=visit_final_E
  # Group by 'FIRST_WORD' and find the most frequent 'VISIT_AREA_NM' for each group
  most_frequent_visits = dfe.groupby('LOTNO_ADDR')['VISIT_AREA_NM'].agg(lambda x: x.mode().iloc[0]).reset_index()

  # Merge the most frequent values back to the original DataFrame based on 'FIRST_WORD'
  dfe = dfe.merge(most_frequent_visits, on='LOTNO_ADDR', how='left', suffixes=('', '_most_frequent'))

  # Update 'VISIT_AREA_NM' with the most frequent values
  dfe['VISIT_AREA_NM'] = dfe['VISIT_AREA_NM_most_frequent'].fillna(dfe['VISIT_AREA_NM'])

  # Drop temporary columns used for grouping and merging
  dfe.drop(columns=['VISIT_AREA_NM_most_frequent'], inplace=True)

  dfe[['TRAVELER_ID', 'VISIT_AREA_NM','ratings','SIDO']]

  # 후처리?
  df1 = dfe.rename(columns={'TRAVELER_ID': 'userID','VISIT_AREA_NM': 'itemID','ratings': 'rating'})

  df1=df1[['userID','itemID','rating','SIDO', 'SI']]
  
  # 'SIDO' 컬럼이 도가 아닌 경우 'SI' 컬럼의 값을 'SIDO'값으로 변경
  df1.loc[~df1['SIDO'].isin(['경남', '경북','제주특별자치도','경기','강원특별자치도','강원','서울','충북','충남','전북','전남']), 'SI'] = df1['SIDO']


  print(df1)

  df1.to_csv("data/preprocessed/여행지/dfE.csv")
  # df1.to_csv("data/preprocessed/여행지/dfF.csv")
  # df1.to_csv("data/preprocessed/여행지/dfG.csv")
  # df1.to_csv("data/preprocessed/여행지/dfH.csv")


    
  return

    
if __name__ == "__main__":
  main()

