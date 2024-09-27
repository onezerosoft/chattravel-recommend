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
  #course = sys.argv[2]
  course = '''{\n" +
                "    \"courseTitle\": \"제주 자연 속으로의 여행\",\n" +
                "    \"day1\": [\n" +
                "        {\"place\": \"제주 신라호텔\", \"reason\": \"\"},\n" +
                "        {\"place\": \"식당1\", \"reason\": \"\"},\n" +
                "        {\"place\": \"카페1\", \"reason\": \"\"},\n" +
                "        {\"place\": \"윗세오름\", \"reason\": \"윗세 오름은 제주의 아름다운 풍경을 한 눈에 볼 수 있는 곳으로, 여행의 시작에 어울립니다.\"},\n" +
                "        {\"place\": \"식당2\", \"reason\": \"\"},\n" +
                "        {\"place\": \"카페2\", \"reason\": \"\"},\n" +
                "        {\"place\": \"섭지코지\", \"reason\": \"섭지코지는 제주의 바다 풍경을 감상할 수 있는 곳으로, 첫날의 마무리로 안성맞춤입니다.\"}\n" +
                "    ],\n" +
                "    \"day2\": [\n" +
                "        {\"place\": \"군산오름 등산로 입구\", \"reason\": \"군산오름 등산로 입구는 푸른 숲속을 걷는 즐거움을 선사하며, 중간 날의 여행을 빛내줍니다.\"},\n" +
                "        {\"place\": \"식당1\", \"reason\": \"\"},\n" +
                "        {\"place\": \"카페1\", \"reason\": \"\"},\n" +
                "        {\"place\": \"강정천\", \"reason\": \"강정천은 맑고 깨끗한 물 소리를 들을 수 있는 자연이 아름다운 곳으로, 중간 날의 여행에 안성맞춤입니다.\"},\n" +
                "        {\"place\": \"식당2\", \"reason\": \"\"},\n" +
                "        {\"place\": \"카페2\", \"reason\": \"\"},\n" +
                "        {\"place\": \"한라산\", \"reason\": \"한라산은 제주의 상징적인 산으로, 중간 날의 여행을 완성해줍니다.\"}\n" +
                "    ],\n" +
                "    \"day3\": [\n" +
                "        {\"place\": \"제주 신라호텔\", \"reason\": \"\"},\n" +
                "        {\"place\": \"식당1\", \"reason\": \"\"},\n" +
                "        {\"place\": \"카페1\", \"reason\": \"\"},\n" +
                "        {\"place\": \"서귀포 치유의 숲\", \"reason\": \"서귀포 치유의 숲은 심신을 안정시키는 힐링 여행지로, 마지막 날에 어울립니다.\"},\n" +
                "        {\"place\": \"식당2\", \"reason\": \"\"},\n" +
                "        {\"place\": \"카페2\", \"reason\": \"\"},\n" +
                "        {\"place\": \"소정방폭포\", \"reason\": \"소정방폭포는 시원한 폭포 소리를 들을 수 있는 아름다운 곳으로, 여행의 마무리를 완성해줍니다.\"}\n" +
                "    ]\n" +
                "}"
            '''

  
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
