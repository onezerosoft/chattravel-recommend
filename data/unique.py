import pickle
import pandas as pd

def sido_unique():
  
  # 수도권
  dfE = pd.read_csv('data/preprocessed/dfE.csv')
  regions_E = dfE['SI'].unique()
  pd.DataFrame(regions_E, columns=['Region']).to_csv('data/unique_list/regions_E.csv', index=False)
        
  
  # 동부권
  dfF = pd.read_csv('data/preprocessed/dfF.csv')
  regions_F = dfF['SI'].unique()
  pd.DataFrame(regions_F, columns=['Region']).to_csv('data/unique_list/regions_F.csv', index=False)
        
  
  # 서부권
  dfG = pd.read_csv('data/preprocessed/dfG.csv')
  regions_G = dfG['SI'].unique()
  pd.DataFrame(regions_G, columns=['Region']).to_csv('data/unique_list/regions_G.csv', index=False)
        
  
  #제주
  dfH = pd.read_csv('data/preprocessed/dfH.csv')
  regions_H = dfH['SI'].unique()
  pd.DataFrame(regions_H, columns=['Region']).to_csv('data/unique_list/regions_H.csv', index=False)
    
  return


def item_unique():
  
  # 수도권
  place_dfE = pd.read_csv('data/preprocessed/여행지/dfE.csv')
  stay_dfE = pd.read_csv('data/preprocessed/숙박/dfE.csv')
  place_E = place_dfE['itemID'].unique()
  stay_E = stay_dfE['itemID'].unique()

  pd.DataFrame(place_E, columns=['itemID']).to_csv('data/unique_list/item/place_E.csv', index=False)
  pd.DataFrame(stay_E, columns=['itemID']).to_csv('data/unique_list/item/stay_E.csv', index=False)
        
  # 동부권
  place_dfF = pd.read_csv('data/preprocessed/여행지/dfF.csv')
  stay_dfF = pd.read_csv('data/preprocessed/숙박/dfF.csv')
  place_F = place_dfF['itemID'].unique()
  stay_F = stay_dfF['itemID'].unique()

  pd.DataFrame(place_F, columns=['itemID']).to_csv('data/unique_list/item/place_F.csv', index=False)
  pd.DataFrame(stay_F, columns=['itemID']).to_csv('data/unique_list/item/stay_F.csv', index=False)
  
  # 서부권
  place_dfG = pd.read_csv('data/preprocessed/여행지/dfG.csv')
  stay_dfG = pd.read_csv('data/preprocessed/숙박/dfG.csv')
  place_G = place_dfG['itemID'].unique()
  stay_G = stay_dfG['itemID'].unique()

  pd.DataFrame(place_G, columns=['itemID']).to_csv('data/unique_list/item/place_G.csv', index=False)
  pd.DataFrame(stay_G, columns=['itemID']).to_csv('data/unique_list/item/stay_G.csv', index=False)
  
  # 제주권
  place_dfH = pd.read_csv('data/preprocessed/여행지/dfH.csv')
  stay_dfH = pd.read_csv('data/preprocessed/숙박/dfH.csv')
  place_H = place_dfH['itemID'].unique()
  stay_H = stay_dfH['itemID'].unique()

  pd.DataFrame(place_H, columns=['itemID']).to_csv('data/unique_list/item/place_H.csv', index=False)
  pd.DataFrame(stay_H, columns=['itemID']).to_csv('data/unique_list/item/stay_H.csv', index=False)
  
    
  return


if __name__ == "__main__":
  item_unique()
