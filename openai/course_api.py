# 코스 생성 
# 1. 여행지 순서 배치
# 2. 여행지별 배치 이유 작성
# 3. 식당&카페 검색 API

import argparse
import openai
import sys
import json

def main():
  
  # with 구문을 사용하여 파일을 열고 닫음
  with open("openai/openai-key.txt", "r", encoding="utf-8") as file:
      openai_key = file.read().strip()  # .strip()을 사용하여 불필요한 공백이나 줄바꿈 제거

  # API 키 설정
  openai.api_key = openai_key

  # user input 생성
  days = sys.argv[1]
  placeList = sys.argv[2]
  region = sys.argv[3]
  accomodation = sys.argv[4]

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

  "days" : {days}
  "placeList" : [{placeList}]


  If "days" is is 1, format the response as a JSON object with the following structure:
  {{
      "courseTitle": "courseTitle"
      "day1": [
          {{"place": "place1", "reason": "reason1"}},
          {{"place": "place2", "reason": "reason2"}},
          {{"place": "place3", "reason": "reason3"}},
      ]
  }}

  If "days" is is not 1, format the response as a JSON object with the following structure:
  {{
      "courseTitle": "courseTitle"
      "day1": [
          {{"place": "place1", "reason": "reason1"}},
          {{"place": "place2", "reason": "reason2"}}
      ],
      "day2": [
          {{"place": "place1", "reason": "reason1"}},
          {{"place": "place2", "reason": "reason2"}},
          {{"place": "place3", "reason": "reason3"}}
      ],
      ...
  }}
  '''

  # GPT-3.5 모델 호출
  response = openai.ChatCompletion.create(
      model="gpt-3.5-turbo",
      messages=[
          {"role": "system", "content": "You are a helpful assistant."},
          {"role": "user", "content": message}
      ]
  )
  result = json.loads(response['choices'][0]['message']['content'])

  


  # 문자열을 JSON으로 변환 (딕셔너리로 매핑)
  result = json.loads(result)
  
  # 식당 & 카페 추가 검색
  for i in range(int(days)):
     day = f"day{i+1}"

     # 당일치기, 중간날 -> 식당&카페 추가
     if int(days) == 1 or (i >0 and i < int(days)-1):
        result[day].insert(1, {"place": "식당1", "reason":""})
        result[day].insert(2, {"place": "카페1", "reason":""})
        result[day].insert(4, {"place": "식당2", "reason":""})
        result[day].insert(5, {"place": "카페2", "reason":""})

     # 첫째날, 마지막날 -> 숙박 추가, 식당&카페 추가
     elif i == 0 or i == int(days) - 1:
        result[day].insert(0, {"place": accomodation, "reason":""})
        result[day].insert(1, {"place": "식당1", "reason":""})
        result[day].insert(2, {"place": "카페1", "reason":""})
        result[day].insert(4, {"place": "식당2", "reason":""})
        result[day].insert(5, {"place": "카페2", "reason":""})

  
  print(json.dumps(result, ensure_ascii=False))
     

if __name__ == "__main__":
    main()
