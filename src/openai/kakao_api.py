import requests
import urllib.parse
from dotenv import load_dotenv
import os
import random

# 기본 키워드 검색 기능
def kakao_local_search(keyword, num, code):

  # .env 파일에서 환경 변수 읽기
  load_dotenv()

  # 환경 변수에서 API 키 가져오기
  kakao_api_key = os.getenv('KAKAO_API_KEY')


  # URL 인코딩된 검색어
  encoded_keyword = urllib.parse.quote(keyword)
  

  # API 요청 URL
  url = f"https://dapi.kakao.com/v2/local/search/keyword.json?query={encoded_keyword}&size={num}&category_group_code={code}"

  # API 요청 헤더
  headers = {
      "Authorization": f"KakaoAK {kakao_api_key}"
  }

  # API 요청 보내기
  try:
      response = requests.get(url, headers=headers)
      response_code = response.status_code
      #print(f"Response Code: {response_code}")

      # 응답 확인
      if response_code == 200:
          #print("Response:", response.json())
          return response.json()["documents"]
      else:
          print(f"Error: {response_code}, {response.text}")

  except Exception as e:
      print(f"An error occurred: {e}")

  return


# 입력으로 들어온 "place"와 가까운 식당과 카페 num개씩 반환 후 랜덤으로 한개 선택
def search_fnb(region, place):
  num = 10
  result = []

  try:
    # 카카오 api 호출
    r_response = kakao_local_search(f"{region} {place} 근처 맛집", num, "FD6")
    c_response = kakao_local_search(f"{region} {place} 근처 카페", num, "CE7")

    # 이름이 여행지랑 같은 거 빼버려
    r_response = [p for p in r_response if p['place_name']!= place]
    c_response = [p for p in c_response if p['place_name']!= place]
    

    # 호출 실패한 경우 -> 지역이름으로 확대해서 재검색
    if len(r_response) == 0:
      r_response = kakao_local_search(f"{region} 맛집", num, "FD6")
      
    if len(c_response) == 0:
      c_response = kakao_local_search(f"{region} 카페", num, "CE7")
      
    r_response = random.sample(r_response,1)
    c_response = random.sample(c_response,1)
    
    
    for r in r_response:
      restaurant = {
        "place":r["place_name"],
        "ratings":"",
        "reason":r["category_name"],
        "address":r["road_address_name"],
        "place_url":r["place_url"]
      }
      result.append(restaurant)

    if len(c_response) == 0:
      cafe = {
        "place":"",
        "ratings":"",
        "reason":"",
        "address":"",
        "place_url":""
      }
      result.append(cafe)

    for c in c_response:
      cafe = {
        "place":c["place_name"],
        "ratings":"",
        "reason":c["category_name"],
        "address":c["road_address_name"],
        "place_url":c["place_url"]
      }
      result.append(cafe)


  except KeyError as e:
    print(f"Response data missing key: {e}")
  except Exception as e:
    print(f"An error occurred: {e}")
  
  print(place +" 검색결과 입니다")
  print(result)

  return result

