# 코스 생성 
# 1. 여행지 순서 배치
# 2. 여행지별 배치 이유 작성
# 3. 식당&카페 검색 API

from openai import OpenAI
import sys
import json
from dotenv import load_dotenv
import kakao_api
import os
import pandas as pd

base_path = "/home/ubuntu/chattravel-server/chattravel-recommend/src/"
#base_path = "src/"

def extract_json_from_text(text):
    try:
        # 첫 번째 중괄호와 마지막 중괄호를 찾아서 추출
        start = text.find('{')
        end = text.rfind('}') + 1
        
        if start == -1 or end == -1:
            print("No JSON found in the text.")
            return None
        
        json_str = text[start:end]
        json_data = json.loads(json_str)
        return json_data
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {e}")
        return None
    
  
# 특정 Item의 정보를 찾는 함수
def get_data(item_name, item_list):
    for item in item_list:
        if item["Item"] == item_name:
            return item["SI"], item["SIDO"], item["PredictedRating"]
    return None



def main():
  # .env 파일에서 환경 변수 읽기
  load_dotenv()

  openai_key = os.getenv('OPENAI_API_KEY')

  # user input 
  user_id = sys.argv[1] # 사용자 아이디
  sido = sys.argv[2] # 여행지 시도
  si = sys.argv[3] # 여행지 시 문자열
  days = sys.argv[4] # 여행일수
  

  file_path = base_path+f"result/prediction_result_{user_id}.json"
  with open(file_path, 'r', encoding='utf-8') as file:
    data = json.load(file)

  placeList = data['place']

  if(days != '1'):
    accommodation = data['accommodation'][0]
  else:
     accommodation = {}

  message = f'''
  "request" 
  - Create a travel course for "days" by arranging destinations on the "placeList." 
  - Arrange 2 destinations for the first and last days and 3 destinations for the middle days
  - If "days" is 1, arrange all three destinations in order
  - Create the best travel course considering the characteristics of the destination and the distance between the destinations. 
  - Write the reasons for the arrangement of the order within the course for each travel destination. 
  - Write it in Korean.
  - All places in "placeList" must be used.
  - Design the distance between places visited on the same day of the course to be close
  - Create a "courseTitle" that tactfully represents the entire course and identifies the {si}.
  - 응답은 다 반말로 친절하게 작성해줘
  - 말투는 즐겁고 귀여운 느낌을 해줘 
  - "accomodation"은 숙소명이야, 이 숙소에 대해 간단한 소개를 반환해줘
  - 내가 준 JSON 형식으로만 대답해

  "days" : {days}
  "placeList" : {placeList}
  "accomodation" : {accommodation}


  If "days" is is 1, format the response as a JSON object with the following structure:
  {{
      "courseTitle": "courseTitle"
      "day1": [
          {{"place":"place1", "reason":"reason1"}},
          {{"place":"place2", "reason":"reason2"}},
          {{"place":"place3", "reason":"reason3"}}
      ]
  }}

  If "days" is is not 1, format the response as a JSON object with the following structure:
  {{
      "courseTitle": "courseTitle"
      "accomodation": "comment"
      "day1": [
          {{"place":"place1", "reason":"reason1"}},
          {{"place":"place2", "reason":"reason2"}}
      ],
      "day2": [
          {{"place":"place1", "reason":"reason1"}},
          {{"place":"place2", "reason":"reason2"}},
          {{"place":"place3", "reason":"reason3"}}
      ],
      ...
  }}
  '''

  # GPT-4 모델 사용
  client = OpenAI(api_key=openai_key)

  completion = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
      {"role": "system", "content": "You are a helpful assistant."},
      {"role": "user", "content": message}  
    ]
  )
  result = extract_json_from_text(completion.choices[0].message.content)
  
  # 식당 & 카페 추가 검색 
  # 개발할거 -> df에서 장소명에 해당하는 si 찾기 & 평점정보
  response = {}
  response["courseTitle"] = result["courseTitle"]
  for i in range(int(days)):
    day = f"day{i+1}"

    d_response = []
    for p in result[day]:
      p_si , p_sido, ratings = get_data(p["place"], placeList)
      p_json = {
        "place":p["place"],
        "ratings":ratings,
        "reason":p["reason"],
        "address":p_sido+" "+p_si,
        "SIDO": p_sido,
        "SI" : p_si,
        "place_url":""
      }
      d_response.append(p_json)

    keword1 = d_response[0]["place"]
    region1 = d_response[0]["SI"]
    keword2 = d_response[1]["place"]
    region2 = d_response[1]["SI"]

    # kakao 검색
    search_result1 = kakao_api.search_fnb(region1, keword1)
    search_result2 = kakao_api.search_fnb(region2, keword2)


    # 당일치기, 중간날 -> 식당&카페 추가
    if int(days) == 1 or (i >0 and i < int(days)-1):
      d_response.insert(1, search_result1[0])
      d_response.insert(2, search_result1[1])
      d_response.insert(4, search_result2[0])
      d_response.insert(5, search_result2[1])

    # 첫째날, 마지막날 -> 숙박 추가, 식당&카페 추가
    elif i == 0 or i == int(days) - 1:
      accommodation_json = {
        "place":accommodation["Item"],
        "ratings":accommodation["PredictedRating"],
        "reason":result["accomodation"],
        "address":accommodation["SIDO"]+ " "+accommodation["SI"],
        "SIDO": accommodation["SIDO"],
        "SI" : accommodation["SI"],
        "place_url":""
      }
      d_response.insert(0, accommodation_json)
      d_response.insert(1, search_result1[0])
      d_response.insert(2, search_result1[1])
      d_response.insert(4, search_result2[0])
      d_response.insert(5, search_result2[1])
      
    response[day] = d_response


  with open(base_path+f"result/course_api_result_{user_id}.json", "w", encoding="utf-8") as f:
        json.dump(response, f, ensure_ascii=False, indent=4)

#   sys.stdout.reconfigure(encoding='utf-8')
#   print(json.dumps(result, ensure_ascii=False))

if __name__ == "__main__":
    main()
