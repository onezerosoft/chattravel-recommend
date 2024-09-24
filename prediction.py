import pickle
import pandas as pd
import os
import sys
import re
import json

def load_model(region):
    base_path = 'model'
    
    if region == 'E':  # 수도권
        place_model_path = os.path.join(base_path, '여행지추천모델', 'svd_model_capital.pkl')
        accommodation_model_path = os.path.join(base_path, '숙소추천모델', 'latent_model_capital.pkl')
    

    elif region == 'F':  # 동부권
        place_model_path = os.path.join(base_path, '여행지추천모델', 'svd_model_east.pkl')
        accommodation_model_path = os.path.join(base_path, '숙소추천모델', 'latent_model_east.pkl')
    
    elif region == 'G':  # 서부권
        place_model_path = os.path.join(base_path, '여행지추천모델', 'svd_model_west.pkl')
        accommodation_model_path = os.path.join(base_path, '숙소추천모델', 'latent_model_west.pkl')
    
    elif region == 'H':  # 제주
        place_model_path = os.path.join(base_path, '여행지추천모델', 'svd_model_jeju.pkl')
        accommodation_model_path = os.path.join(base_path, '숙소추천모델', 'latent_model_jeju.pkl')
    
    else:
        raise ValueError("Invalid region code. Please use 'E', 'F', 'G', or 'H'.")
    
    place_model = pickle.load(open(place_model_path, 'rb'))
    accommodation_model = pickle.load(open(accommodation_model_path, 'rb'))

    return place_model, accommodation_model


def load_data(si):
    
    df1 = pd.read_csv('data/preprocessed/여행지/df_total.csv')
    df2 = pd.read_csv('data/preprocessed/숙박/df_total.csv')
        
    df1 = df1[df1['SI'].isin(si)]
    df2 = df2[df2['SI'].isin(si)]
    
    return df1, df2


def predict_place(model, df, user_id, num):
    
    items_to_predict = df['itemID'].unique()

    # 사용자가 방문하지 않은 아이템에 대한 예측 생성
    #all_items = df1['itemID'].unique()
    #user_items = df1[df1['userID'] == user_id]['itemID'].unique()
    #items_to_predict = [item for item in all_items if item not in user_items]

    # 각 아이템에 대해 예측 수행
    predictions = [model.predict(user_id, item) for item in items_to_predict]

    # 예측된 점수로 정렬하여 상위 N개의 아이템 추천
    top_n_predictions = sorted(predictions, key=lambda x: x.est, reverse=True)[:num]

    # 추천 결과 
    result = []
    for prediction in top_n_predictions:
        result.append({
           "Item": prediction.iid,
           "PredictedRating": prediction.est
        })
    
    return result


def predict_accommodation(model, df, user_id, num):
    items_to_predict = df['itemID'].unique()

    # 사용자가 방문하지 않은 아이템에 대한 예측 생성
    #all_items = df1['itemID'].unique()
    #user_items = df1[df1['userID'] == user_id]['itemID'].unique()
    #items_to_predict = [item for item in all_items if item not in user_items]

    # 각 아이템에 대해 예측 수행
    predictions = [model.predict(user_id, item) for item in items_to_predict]

    # 예측된 점수로 정렬하여 상위 N개의 아이템 추천
    top_n_predictions = sorted(predictions, key=lambda x: x.est, reverse=True)[:num]

  
    # 추천 결과 
    result = []
    for prediction in top_n_predictions:
        result.append({
           "Item": prediction.iid,
           "PredictedRating": prediction.est
        })
    
    return result


def main():

    user_id = sys.argv[1] # 사용자 아이디
    sido = sys.argv[2] # 여행지 시도
    si = re.split(r',\s*', sys.argv[3].strip('[]')) # 여행지 시(군) 리스트
    day = int(sys.argv[4]) # 여행일수

    # 여행지 / 숙박지 추천 갯수
    if day == 1:  #당일치기
      place_num = 3 
      accom_num = 0 
    else:
      place_num = day * 3 - 2
      accom_num = 1     

    # region
    if sido in ["서울", "경기도", "강원도"]:
      region = 'E'

    elif sido in ["경상북도", "경상남도"]:
      region = 'F'

    elif sido in ["충청북도", "충청남도", "전라북도", "전라남도"]:
      region = 'G'
    
    elif sido in ["제주도"]:
      region = 'H'
    

    # 지역별 추천 모델과 데이터 불러오기
    place_model, accommodation_model = load_model(region)
    df1 , df2 = load_data(si)

    
    # 여행지 추천 모델
    place_predictions = predict_place(place_model, df1, user_id, place_num)

    # 숙박 장소 추천 모델
    accommodation_predictions = predict_accommodation(accommodation_model, df2, user_id, accom_num)

    result = {
       "place": place_predictions,
       "accommodation": accommodation_predictions
    }

    print(json.dump(result, ensure_ascii=False))

if __name__ == "__main__":
    main()
  