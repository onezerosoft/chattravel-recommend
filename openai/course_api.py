# 코스 생성 
# 1. 여행지 순서 배치
# 2. 여행지별 배치 이유 작성

import argparse
import openai

# ArgumentParser 객체 생성
parser = argparse.ArgumentParser(description="Process days and placeList")
parser.add_argument('--days', type=int, required=True, help="Number of days")
parser.add_argument('--placeList', type=lambda s: s.split(','), required=True, help="Comma-separated list of places")
parser.add_argument('--region', type=str, required=True, help="region")

args = parser.parse_args()

# with 구문을 사용하여 파일을 열고 닫음
with open("openai/openai-key.txt", "r", encoding="utf-8") as file:
    openai_key = file.read().strip()  # .strip()을 사용하여 불필요한 공백이나 줄바꿈 제거

# API 키 설정
openai.api_key = openai_key

# user input 생성
days = args.days
placeList = args.placeList
region = args.region

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

# 응답 출력
print(response['choices'][0]['message']['content'])
