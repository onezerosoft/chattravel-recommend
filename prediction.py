import pickle
import pandas as pd
import os
import sys

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


def load_data(region, si):
    
    if region == 'E':  # 수도권
        df1 = pd.read_csv('data/preprocessed/여행지/dfE.csv')
        df2 = pd.read_csv('data/preprocessed/숙박/dfE.csv')
    
    elif region == 'F':  # 동부권
        df1 = pd.read_csv('data/preprocessed/여행지/dfF.csv')
        df2 = pd.read_csv('data/preprocessed/숙박/dfF.csv')
    
    elif region == 'G':  # 서부권
        df1 = pd.read_csv('data/preprocessed/여행지/dfG.csv')
        df2 = pd.read_csv('data/preprocessed/숙박/dfG.csv')
    
    elif region == 'H':  # 제주
        df1 = pd.read_csv('data/preprocessed/여행지/dfH.csv')
        df2 = pd.read_csv('data/preprocessed/숙박/dfH.csv')
    
    else:
        raise ValueError("Invalid region code. Please use 'E', 'F', 'G', or 'H'.")
    
    df1 = df1[df1['SI']==si]
    df2 = df2[df2['SI']==si]
    
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

    # 추천 결과 출력
    
    print("추천 여행지")
    for prediction in top_n_predictions:
        #print(prediction)
        print(f"Item: {prediction.iid}, Predicted Rating: {prediction.est}")
    
    print(" ")
    
    return top_n_predictions


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

    # 추천 결과 출력
    print("추천 숙박지")
    for prediction in top_n_predictions:
        #print(prediction)
        print(f"Item: {prediction.iid}, Predicted Rating: {prediction.est}")
    print(" ")
    
    return top_n_predictions


def main():

    region = sys.argv[1]
    si = sys.argv[2] # 여행지 시(군)
    place_num = int(sys.argv[3]) # 추천 여행지 갯수
    accom_num = int(sys.argv[4]) # 추천 숙박지 갯수

  
    # 지역별 추천 모델과 데이터 불러오기
    place_model, accommodation_model = load_model(region)
    df1 , df2 = load_data(region, si)

    # 사용자 아이디
    user_id = 'h000617'
    
    # 여행지 추천 모델
    place_predictions = predict_place(place_model, df1, user_id, place_num)

    # 숙박 장소 추천 모델
    user_id = 'h_h000617'
    accommodation_predictions = predict_accommodation(accommodation_model, df2, user_id, accom_num)

    
if __name__ == "__main__":
    main()
