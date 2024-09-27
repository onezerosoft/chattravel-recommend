# 채팅기능 
# 1. 유저의 요구사항 파악
# 2. 챗봇 페르소나 기반 응답 생성

import argparse
import openai
import sys

def main():
  # with 구문을 사용하여 파일을 열고 닫음
  with open("openai/openai-key.txt", "r", encoding="utf-8") as file:
      openai_key = file.read().strip()  # .strip()을 사용하여 불필요한 공백이나 줄바꿈 제거

  # API 키 설정
  openai.api_key = openai_key

  # 인자 파싱
  userMessage = sys.argv[1]
  course = sys.argv[2]
  
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
  - Return the service's number and its response together.
  - If "function" is 1 or 2 or 3, create a changed course, keeping the format of "currentCourse" intact.
  - If "function" is 4 or 5, Return that information.
  - Don't give me information you don't know
  - If you can't find the service requested by the user (function: 6), use "role" to generate an appropriate response.
  - Write it in Korean.
  - Write in a bright and kind way.
  - Respond in a friendly informal manner
  
  "userMessage" : {userMessage}
  "currentCourse" : {course}

  Format the response as a JSON object with the following structure:
  If "function" is 1 or 2 or 3, 
  {{
    "function": "functionNumber"
    "response": {{
      "courseTitle": "courseTitle"
      "day1": [
          {{"place": "place1", "reason": "reason1"}},
          {{"place": "place2", "reason": "reason2"}},
          {{"place": "place3", "reason": "reason3"}},
          {{"place": "place4", "reason": "reason4"}},
          {{"place": "place5", "reason": "reason5"}},
          {{"place": "place6", "reason": "reason6"}},
          {{"place": "place7", "reason": "reason7"}},
      ],
      ...
    }}
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


  # GPT-4 모델 사용 예시
  response = openai.ChatCompletion.create(
      model="gpt-4-1106-preview",
      messages=[
          {"role": "system", "content": "You are a helpful assistant."},
          {"role": "user", "content": message}
      ]
  )

  # 응답 출력
  print(response['choices'][0]['message']['content'])


if __name__ == "__main__":
    main()
