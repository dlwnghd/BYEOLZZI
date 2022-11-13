import requests
from random import randint, sample, shuffle

class Around():
    def __init__(self, db) -> None:
        self.api_key = f"T2C2FcGwTQsDBpFIsNAZ%2FMN610NX4FJls93RmihKvCvvbWV29Nlf5iMEY0OCp2iOdIYN%2BAx44NfOm6eK9cqNkg%3D%3D"
        self.areaCode = None
        self.sigunguCode = None
        self.db = db

    def search_around(self, location):
        print('location:', location)
        sql = "select metro_code, location_code from location where location like '{}%'".format(location)
        search_answer = self.db.select_all(sql)

        print("sql:", sql)
        print("answer:", search_answer)

        self.areaCode = search_answer[0]['metro_code']
        self.sigunguCode = search_answer[0]['location_code']

        print("areaCode:", self.areaCode)
        print("sigunguCode:", self.sigunguCode)
        
        url = f"https://apis.data.go.kr/B551011/KorService/areaBasedList?serviceKey={self.api_key}&numOfRows=15&pageNo=1&MobileOS=ETC&MobileApp=AppTest&_type=json&listYN=Y&arrange=C&contentTypeId=12&areaCode={self.areaCode}&sigunguCode={self.sigunguCode}"
        response = requests.get(url, verify=False)

        try:
            around = response.json()
            around_list = around['response']['body']['items']['item']
        except Exception as e:
            print(e)
        around_data = [
            {
            'title' : area['title'],
            'addr' : area['addr1'] + area['addr2'],
            # 'areaCode' : self.areaCode,
            # 'sigunguCode' : self.sigunguCode,
            'mapx' : area['mapx'],
            'mapy' : area['mapy']
            }
            for area in around_list
        ]
        print(around_data)
        shuffle(around_data)
        around_data = sample(around_data, 3)

        return around_data