# 채팅기능 
# 1. 유저의 요구사항 파악
# 2. 챗봇 페르소나 기반 응답 생성

import openai
import sys
import json
import os
from dotenv import load_dotenv
import re

def extract_json_from_text(text):
    json_pattern = re.compile(r'\{(?:[^{}]|(?R))*\}')
    match = json_pattern.search(text)
    
    if match:
        json_str = match.group()
        try:
            json_data = json.loads(json_str)
            return json_data
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON: {e}")
            return None
    else:
        print("No JSON found in the text.")
        return None

def main():
  # .env 파일에서 환경 변수 읽기
  load_dotenv()

  openai_key = os.getenv('OPENAI_API_KEY')

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
  response = extract_json_from_text(response['choices'][0]['message']['content'])
  
  result = json.loads(response)

  with open("chattravel-recommend/src/result/chat_api_result.json", "w", encoding="utf-8") as f:
      json.dump(result, f, ensure_ascii=False, indent=4)

#     sys.stdout.reconfigure(encoding='utf-8')
#     print(json.dumps(result, ensure_ascii=False))

if __name__ == "__main__":
    main()
