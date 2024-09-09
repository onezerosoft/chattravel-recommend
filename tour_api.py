import requests
import os
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

TOUR_URL = "http://apis.data.go.kr/B551011/Durunubi"

# API 기본 설정
class TourAPI:
    def __init__(self):
        self.base_url = TOUR_URL
        self.params = {
            "serviceKey": os.getenv("DURUNUBI_TOUR_SERVICE_KEY"),
            "numOfRows": 3,
            "pageNo": 10,
            "_type": "json",
            "MobileOS": "IOS",
            "MobileApp": "chattravel",
        }

    def get(self, endpoint):
        response = requests.get(f"{self.base_url}{endpoint}", params=self.params)
        response.raise_for_status()  
        return response.json()

tour_api = TourAPI()

# 코스 목록 정보 조회
def get_course_list():
    
    try:
        data = tour_api.get("/courseList")
        return data["response"]["body"]["items"]["item"]
    except Exception as e:
        raise RuntimeError("Failed to fetch courseList") from e

# 길 목록 정보 조회
def get_route_list():
    try:
        data = tour_api.get("/routeList")
        # print(data)
        return data["response"]["body"]
    except Exception as e:
        raise RuntimeError("Failed to fetch routeList") from e

if __name__ == "__main__":
    # 실행 테스트
    try:
        course_list = get_course_list()
        for course in course_list:
            print(course)
        
        route_list = get_route_list()
    except RuntimeError as e:
        print(e)
