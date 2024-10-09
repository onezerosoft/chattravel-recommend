# 채팅기능 
# 1. 유저의 요구사항 파악
# 2. 챗봇 페르소나 기반 응답 생성

from openai import OpenAI
import sys
import json
import os
from dotenv import load_dotenv
import re

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
    

def main():
  # # .env 파일에서 환경 변수 읽기
  # load_dotenv()

  # openai_key = os.getenv('OPENAI_API_KEY')

  # # API 키 설정
  # openai.api_key = openai_key

  # with 구문을 사용하여 파일을 열고 닫음
  # with open(base_path+"openai/openai-key.txt", "r", encoding="utf-8") as file:
  #     openai_key = file.read().strip()  # .strip()을 사용하여 불필요한 공백이나 줄바꿈 제거

  # API 키 설정
  #openai.api_key = openai_key


  # 인자 파싱
  userMessage = sys.argv[1]
  chatId = sys.argv[2]

  with open(base_path+f"result/course_args_{chatId}.txt", "r", encoding="utf-8") as f:
    course = f.read()

  course_format = extract_json_from_text(course)

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
  client = OpenAI()

  completion = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
      {"role": "system", "content": "You are a helpful assistant."},
      {"role": "user", "content": message}  
    ]
  )
  result = extract_json_from_text(completion.choices[0].message.content)

  with open(base_path+f"result/chat_api_result_{chatId}.json", "w", encoding="utf-8") as f:
      json.dump(result, f, ensure_ascii=False, indent=4)

#     sys.stdout.reconfigure(encoding='utf-8')
#     print(json.dumps(result, ensure_ascii=False))

if __name__ == "__main__":
    main()
