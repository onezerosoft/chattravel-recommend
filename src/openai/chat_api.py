# 채팅기능 
# 1. 유저의 요구사항 파악
# 2. 챗봇 페르소나 기반 응답 생성

import argparse
import openai
import sys
import json
import os

def clear_json_content(json_obj):
    if isinstance(json_obj, dict):
        return {key: clear_json_content(value) for key, value in json_obj.items()}
    elif isinstance(json_obj, list):
        return [clear_json_content(item) for item in json_obj]
    else:
        # 내용 제거 (None으로 설정하거나 빈 문자열, 빈 리스트 등으로 설정 가능)
        return "content"  

def main():
  # with 구문을 사용하여 파일을 열고 닫음
  with open("chattravel-recommend/src/openai/openai-key.txt", "r", encoding="utf-8") as file:
      openai_key = file.read().strip()  # .strip()을 사용하여 불필요한 공백이나 줄바꿈 제거

  # API 키 설정
  openai.api_key = openai_key

  # 인자 파싱
  userMessage = sys.argv[1]

  with open("chattravel-recommend/src/result/course_args.txt", "r", encoding="utf-8") as f:
    course = f.read()

  clean_json = clear_json_content(json.loads(course))
  course_format = json.dumps(clean_json, indent=2)  

  message = f'''
  "role":
  You're the travel arrangement assistant, "챗트".
  You have a kind and friendly personality.
  You are a travel counselor who knows many people's travel information.
  You help create new travel plans, or modify them.
  You give additional information such as operating hours and admission fees of the travel destination.
  You can guide the necessary supplies at the travel destination.

  "functionList":[
    1: "Travel Course Reset",
    2: "Change of destination",
    3: "Change the destination order",
    4: "Operating Hours Information"
    5: "Adimission fee information"
    6: "Desired features not found"
  ]

  "request":
  - Read the "userMessage", select the service the user wants from the "functionList".
  - If "function" is 1 or 2 or 3, create a changed course, keeping the format of "currentCourse" intact.
  - Find a real recommended destination and complete the course
  - If "function" is 4 or 5, Return that information.
  - Don't give me information you don't know
  - If you can't find the service requested by the user (function: 6), use "role" to generate an appropriate response.
  - Write it in Korean.
  - Write in a bright and kind way.
  - Respond in a friendly informal manner
  - 응답은 다 반말로 친절하게 작성해줘
  
  "userMessage" : {userMessage}
  "currentCourse" : {course}

  Format the response as a JSON object with the following structure:
  첨부한 "course_format" 형식을 반드시 지켜서 작성해
  If "function" is 1 or 2 or 3, 
  {{
    "function": "functionNumber"
    "response": {course_format}
  }}
  
  If "function" is 4 or 5,  
  {{
    "function": "functionNumber"
    "response": "information message"
  }}
  
  If "function" is 6,  
  {{
    "function": "functionNumber"
    "response": "response message"
  }}
  '''


  # GPT-4 모델 사용
  response = openai.ChatCompletion.create(
      model="gpt-4-1106-preview",
      messages=[
          {"role": "system", "content": "You are a helpful assistant."},
          {"role": "user", "content": message}
      ]
  )
  response = response['choices'][0]['message']['content']

  # 마크다운 표기 제거 (앞의 ```json와 끝의 ``` 제거)
  clean_json_string = response.strip('```json\n').strip('```')
  
  result = json.loads(clean_json_string)


  with open("chattravel-recommend/src/result/chat_api_result.json", "w", encoding="utf-8") as f:
      json.dump(result, f, ensure_ascii=False, indent=4)

#     sys.stdout.reconfigure(encoding='utf-8')
#     print(json.dumps(result, ensure_ascii=False))

if __name__ == "__main__":
    main()
