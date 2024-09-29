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

  # message = f'''
  # "request" 
  # - Create a travel course for "days" by arranging destinations on the "placeList." 
  # - Arrange 2 destinations for the first and last days and 3 destinations for the middle days
  # - If "days" is 1, arrange all three destinations in order
  # - Create the best travel course considering the characteristics of the destination and the distance between the destinations. 
  # - Write the reasons for the arrangement of the order within the course for each travel destination. 
  # - Write it in Korean.
  # - Write in a bright and kind way.
  # - All places in "placeList" must be used.
  # - Design the distance between places visited on the same day of the course to be close
  # - Create a "courseTitle" that tactfully represents the entire course and identifies the {region}.
  # - 응답은 다 반말로 친절하게 작성해줘
  # - 각 장소에 대한 주소와 카카오맵 URL도 함께 보내
  # - "accomodation"은 숙소명이야, 간략한 설명과 숙소 주소, 카카오맵 URL도 보내
  # - 내가 준 JSON 형식으로만 대답해

  # "days" : {days}
  # "placeList" : [{placeList}]
  # "accomodation" : {accomodation}


  # If "days" is is 1, format the response as a JSON object with the following structure:
  # {{
  #     "courseTitle": "courseTitle"
  #     "accomodation":{{"comment":"간략한 설명","address":"address1", "place_url":"url1"}}
  #     "day1": [
  #         {{"place":"place1", "reason":"reason1", "address":"address1", "place_url":"url1"}},
  #         {{"place":"place2", "reason":"reason2", "address":"address2", "place_url":"url2"}},
  #         {{"place":"place3", "reason":"reason3", "address":"address3", "place_url":"url3"}}
  #     ]
  # }}

  # If "days" is is not 1, format the response as a JSON object with the following structure:
  # {{
  #     "courseTitle": "courseTitle"
  #     "accomodation":{{"address":"address1", "place_url":"url1"}}
  #     "day1": [
  #         {{"place":"place1", "reason":"reason1", "address": "address1", "place_url":"url1"}},
  #         {{"place":"place2", "reason":"reason2", "address": "address2", "place_url":"url2"}}
  #     ],
  #     "day2": [
  #         {{"place":"place1", "reason":"reason1", "address":"address1", "place_url":"url1"}},
  #         {{"place":"place2", "reason":"reason2", "address":"address2", "place_url":"url2"}},
  #         {{"place":"place3", "reason":"reason3", "address":"address3", "place_url":"url3"}}
  #     ],
  #     ...
  # }}
  # '''

  # # GPT-4 모델 
  # response = openai.ChatCompletion.create(
  #     model="gpt-4-1106-preview",
  #     messages=[
  #         {"role": "system", "content": "You are a helpful assistant."},
  #         {"role": "user", "content": message}
  #     ]
  # )
  # result = extract_json_from_text(response['choices'][0]['message']['content'])
  
  # print(result)

  result = "{'courseTitle': '제주여행의 힐링 코스: 숲과 오름을 넘나들며', 'accomodation': {'address': '제주특별자치도 제주시 천제연로 72 제주 신라호텔', 'place_url': 'https://place.map.kakao.com/2731247'}, 'day1': [{'place': '군산오름 등산로 입구', 'reason': '첫째 날은 가벼운 산책으로 시작해서 몸을 풀어주자구. 군산오름도 접근성 좋고 경치가 예뻐!', 'address': '제주특별자치도 서귀포시 대정읍', 'place_url': 'https://place.map.kakao.com/12646602'}, {'place': '소정방폭포', 'reason': '군산오름에서 멀지 않고, 폭포 소리 들으며 정신적으로 힐링하기 좋아!', 'address': '제주특별자치도 서귀포시 소정방로', 'place_url': 'https://place.map.kakao.com/7882681'}], 'day2': [{'place': '한라산', 'reason': '둘째 날은 제대로 활력 충전! 한라산 등반하며 제주의 자연을 만끽하자!', 'address': '제주특별자치도 제주시 1100로 2070-61', 'place_url': 'https://place.map.kakao.com/26533254'}, {'place': '윗세오름', 'reason': '한라산 내려와서 가까운 윗세오름으로, 오름 정 상에서 탁 트인 전망 즐기고!', 'address': '제주특별자치도 제주시 아라동', 'place_url': 'https://place.map.kakao.com/12862695'}, {'place': '서귀포 치유의 숲', 'reason': '하루 일정 마무리는 치유의 숲에서 상쾌한 공기 마시며 휴식을~', 'address': '제주특별자치도 서귀포시 남원읍 신례로 153', 'place_url': 'https://place.map.kakao.com/26916059'}], 'day3': [{'place': '강정천', 'reason': '셋째 날은 조금 여유를 갖고 강정천에서 맑은 물소리를 들으며 평화롭게 걸어보자.', 'address': '제주특별자치도 서귀포시 강정동', 'place_url': 'https://place.map.kakao.com/10249015'}, {'place': '섭지코지', 'reason': '제주 동쪽 끝자락에 위치한 섭지 코지, 바다와 함께 멋진 사진 기념으로 남기기 딱이야!', 'address': '제주특별자치도 서귀포시 성산읍 섭지코지로 107', 'place_url': 'https://place.map.kakao.com/7831963'}]}"
  result = json.loads(result.replace("'", '"'))

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

  print("...")
  print(result)

  with open("chattravel-recommend/src/result/course_api_result.json", "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=4)

#   sys.stdout.reconfigure(encoding='utf-8')
#   print(json.dumps(result, ensure_ascii=False))

if __name__ == "__main__":
    main()
