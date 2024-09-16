import openai

# with 구문을 사용하여 파일을 열고 닫음
with open("openai-key.txt", "r", encoding="utf-8") as file:
    openai_key = file.read().strip()  # .strip()을 사용하여 불필요한 공백이나 줄바꿈 제거

# API 키 설정
openai.api_key = openai_key

# GPT-4 모델 사용 예시
response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Tell me something interesting."},
    ]
)

# 응답 출력
print(response['choices'][0]['message']['content'])
