import pickle
import pandas as pd
import os
import sys
import re
import json

base_path = '/home/ubuntu/chattravel-server/chattravel-recommend/src/'
#base_path = 'src/' # 이거는 chattravel-recommend에서 테스트 할떄


def load_model(region):

    #print(os.getcwd())
    
    if region == 'E':  # 수도권
        place_model_path = os.path.join(base_path, 'model', 'place', 'svd_model_capital.pkl')
        accommodation_model_path = os.path.join(base_path, 'model', 'accomodation', 'latent_model_capital.pkl')
    

    elif region == 'F':  # 동부권
        place_model_path = os.path.join(base_path, 'model', 'place', 'svd_model_east.pkl')
        accommodation_model_path = os.path.join(base_path, 'model', 'accomodation', 'latent_model_east.pkl')
    
    elif region == 'G':  # 서부권
        place_model_path = os.path.join(base_path, 'model', 'place', 'svd_model_west.pkl')
        accommodation_model_path = os.path.join(base_path, 'model', 'accomodation', 'latent_model_west.pkl')
    
    elif region == 'H':  # 제주
        place_model_path = os.path.join(base_path, 'model', 'place', 'svd_model_jeju.pkl')
        accommodation_model_path = os.path.join(base_path, 'model', 'accomodation', 'latent_model_jeju.pkl')
    
    else:
        raise ValueError("Invalid region code. Please use 'E', 'F', 'G', or 'H'.")
    
    place_model = pickle.load(open(place_model_path, 'rb'))
    accommodation_model = pickle.load(open(accommodation_model_path, 'rb'))

    return place_model, accommodation_model


def load_data(si):
    
    df1 = pd.read_csv(base_path+'data/preprocessed/place/df_total.csv')
    df2 = pd.read_csv(base_path+'/data/preprocessed/accomodation/df_total.csv')
        
    df1 = df1[df1['SI'].isin(si)]
    df2 = df2[df2['SI'].isin(si)]
    
    return df1, df2


def predict_place(model, df, user_id, num, si):
    
    items_to_predict = df['itemID'].unique()

    # 사용자가 방문하지 않은 아이템에 대한 예측 생성
    all_items = df['itemID'].unique()
    user_items = df[df['userID'] == user_id]['itemID'].unique()
    items_to_predict = [item for item in all_items if item not in user_items]

    # 각 아이템에 대해 예측 수행
    predictions = [model.predict(user_id, item) for item in items_to_predict]

    # SI 필터링
    #print(predictions)
    #predictions = predictions[predictions['SI'].isin(si)]

    # 예측된 점수로 정렬하여 상위 N개의 아이템 추천
    top_n_predictions = sorted(predictions, key=lambda x: x.est, reverse=True)[:num]

    # 추천 결과 
    result = []
    for prediction in top_n_predictions:
        percentage = (prediction.est / 5) * 100
        result.append({
           "Item": prediction.iid,
           "PredictedRating": round(percentage, 2)
        })
    
    return result


def predict_accommodation(model, df, user_id, num, si):
    items_to_predict = df['itemID'].unique()

    # 사용자가 방문하지 않은 아이템에 대한 예측 생성
    all_items = df['itemID'].unique()
    user_items = df[df['userID'] == user_id]['itemID'].unique()
    items_to_predict = [item for item in all_items if item not in user_items]

    # 각 아이템에 대해 예측 수행
    predictions = [model.predict(user_id, item) for item in items_to_predict]

    # SI 필터링
    #print(predictions)
    #predictions = predictions[predictions['SI'].isin(si)]

    # 예측된 점수로 정렬하여 상위 N개의 아이템 추천
    top_n_predictions = sorted(predictions, key=lambda x: x.est, reverse=True)[:num]

  
    # 추천 결과 
    result = []
    for prediction in top_n_predictions:
        percentage = (prediction.est / 5) * 100
        result.append({
           "Item": prediction.iid,
           "PredictedRating": round(percentage, 2)
        })
    
    return result

def insert_dummy_data(df):
   
   
   return


def main():
    
    user_id = sys.argv[1] # 사용자 아이디
    sido = sys.argv[2] # 여행지 시도
    si = re.split(r',\s*', sys.argv[3].strip('[]')) # 여행지 시(군) 리스트
    day = int(sys.argv[4]) # 여행일수
    styleList = list(map(int, re.split(r',\s*', sys.argv[5].strip('[]'))))
    
    # 여행지 / 숙박지 추천 갯수
    if day == 1:  #당일치기
      place_num = 3 
      accom_num = 0 
    else:
      place_num = day * 3 - 2 
      accom_num = 1     

    # region
    if sido in ["서울", "경기도", "강원도", "수도권"]:
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
    
    # 여행 스타일 별 더미데이터 삽입
    dummy_df = pd.read_csv(base_path+'/data/style/dummy_data.csv')
    categories = [['자연', '도시'], ['관광', '휴식'], ['사진O', '사진X'], ['럭셔리숙박', '가성비숙박']]
    
    for i in range(4):
        style = styleList[i]
        a, b = categories[i]
        
        random_rows_a = dummy_df[dummy_df['category'] == a].sample(n=20)
        random_rows_b = dummy_df[dummy_df['category'] == b].sample(n=20)
        random_rows_a['rating'] = 6-style
        random_rows_b['rating'] = style
        random_rows_a['userID'] = user_id
        random_rows_b['userID'] = user_id
        random_rows_a = random_rows_a.drop(columns=['category'])
        random_rows_b = random_rows_b.drop(columns=['category'])
        
        if i < 3:
            df1 = pd.concat([df1, random_rows_a, random_rows_b], ignore_index=True)
        else: 
            df2 = pd.concat([df2, random_rows_a, random_rows_b], ignore_index=True)
    
    # 여행지 추천 모델
    place_predictions = predict_place(place_model, df1, user_id, place_num, si)

    # 숙박 장소 추천 모델
    accommodation_predictions = predict_accommodation(accommodation_model, df2, user_id, accom_num, si)

    result = {
       "place": place_predictions,
       "accommodation": accommodation_predictions
    }

    with open(base_path+f"result/prediction_result_{user_id}.json", "w", encoding="utf-8") as f:
      json.dump(result, f, ensure_ascii=False, indent=4)

#     sys.stdout.reconfigure(encoding='utf-8')
#     print(json.dumps(result, ensure_ascii=False))

if __name__ == "__main__":
    main()
  