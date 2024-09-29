# 코스 생성 
# 1. 여행지 순서 배치
# 2. 여행지별 배치 이유 작성
# 3. 식당&카페 검색 API

import openai
import sys
import json
from dotenv import load_dotenv
import os
import kakao_api
import re

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
    

def main():
  # .env 파일에서 환경 변수 읽기
  load_dotenv()

  openai_key = os.getenv('OPENAI_API_KEY')

  # API 키 설정
  openai.api_key = openai_key

  # user input 생성
  days = sys.argv[1]
  placeList = sys.argv[2]
  accomodation = sys.argv[3]
  region = sys.argv[4]

  message = f'''
  "request" 
  - Create a travel course for "days" by arranging destinations on the "placeList." 
  - Arrange 2 destinations for the first and last days and 3 destinations for the middle days
  - If "days" is 1, arrange all three destinations in order
  - Create the best travel course considering the characteristics of the destination and the distance between the destinations. 
  - Write the reasons for the arrangement of the order within the course for each travel destination. 
  - Write it in Korean.
  - Write in a bright and kind way.
  - All places in "placeList" must be used.
  - Design the distance between places visited on the same day of the course to be close
  - Create a "courseTitle" that tactfully represents the entire course and identifies the {region}.
  - 응답은 다 반말로 친절하게 작성해줘
  - 각 장소에 대한 주소와 카카오맵 URL도 함께 보내
  - "accomodation"은 숙소명이야, 간략한 설명과 숙소 주소, 카카오맵 URL도 보내
  - 내가 준 JSON 형식으로만 대답해

  "days" : {days}
  "placeList" : [{placeList}]
  "accomodation" : {accomodation}


  If "days" is is 1, format the response as a JSON object with the following structure:
  {{
      "courseTitle": "courseTitle"
      "accomodation":{{"comment":"간략한 설명","address":"address1", "place_url":"url1"}}
      "day1": [
          {{"place":"place1", "reason":"reason1", "address":"address1", "place_url":"url1"}},
          {{"place":"place2", "reason":"reason2", "address":"address2", "place_url":"url2"}},
          {{"place":"place3", "reason":"reason3", "address":"address3", "place_url":"url3"}}
      ]
  }}

  If "days" is is not 1, format the response as a JSON object with the following structure:
  {{
      "courseTitle": "courseTitle"
      "accomodation":{{"address":"address1", "place_url":"url1"}}
      "day1": [
          {{"place":"place1", "reason":"reason1", "address": "address1", "place_url":"url1"}},
          {{"place":"place2", "reason":"reason2", "address": "address2", "place_url":"url2"}}
      ],
      "day2": [
          {{"place":"place1", "reason":"reason1", "address":"address1", "place_url":"url1"}},
          {{"place":"place2", "reason":"reason2", "address":"address2", "place_url":"url2"}},
          {{"place":"place3", "reason":"reason3", "address":"address3", "place_url":"url3"}}
      ],
      ...
  }}
  '''

  # GPT-4 모델 
  response = openai.ChatCompletion.create(
      model="gpt-4-1106-preview",
      messages=[
          {"role": "system", "content": "You are a helpful assistant."},
          {"role": "user", "content": message}
      ]
  )
  result = extract_json_from_text(response['choices'][0]['message']['content'])
  

  # 식당 & 카페 추가 검색 
  for i in range(int(days)):
    day = f"day{i+1}"

    keword1 = result[day][0]["place"]
    keword2 = result[day][1]["place"]

    # kakao 검색
    search_result1 = kakao_api.search_fnb(region, keword1)
    search_result2 = kakao_api.search_fnb(region, keword2)


    # 당일치기, 중간날 -> 식당&카페 추가
    if int(days) == 1 or (i >0 and i < int(days)-1):
      result[day].insert(1, search_result1[0])
      result[day].insert(2, search_result1[1])
      result[day].insert(4, search_result2[0])
      result[day].insert(5, search_result2[1])

    # 첫째날, 마지막날 -> 숙박 추가, 식당&카페 추가
    elif i == 0 or i == int(days) - 1:
      accomodation_json = {
        "place":accomodation,
        "reason":"",
        "address":result["accomodation"]["address"],
        "place_url":result["accomodation"]["place_url"]
      }
      result[day].insert(0, accomodation_json)
      result[day].insert(1, search_result1[0])
      result[day].insert(2, search_result1[1])
      result[day].insert(4, search_result2[0])
      result[day].insert(5, search_result2[1])


  with open("chattravel-recommend/src/result/course_api_result.json", "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=4)

#   sys.stdout.reconfigure(encoding='utf-8')
#   print(json.dumps(result, ensure_ascii=False))

if __name__ == "__main__":
    main()
