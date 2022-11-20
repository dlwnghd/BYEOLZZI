import requests
import datetime
from utils.Database import Database
class festival:
    def __init__(self, db=None):
        self.db = db

    def fes_sum(self, location):
        now = datetime.datetime.now()
        date= now.strftime("%Y")+now.strftime("%m")+now.strftime("%d")
        key = "2qOlMnHP2j9Bjvyo6tdhQNCDu9%2Bh1mm3LS9V2hXPxHfCrPW73YsGnPOrmYt1BnDjUXWywI2gOrz9c7fvwYeBHw%3D%3D"
        sql = "select * from location where location like '{}%';".format(location)
        print("sql :",sql)
        want = self.db.select_all(sql)
        print("뽑은 값:",want)

        try:
            met_code = want[0]['metro_code']
            loc_code= want[0]['location_code']
            print("지역코드 : ",loc_code)
            url=f'https://apis.data.go.kr/B551011/KorService/searchFestival?serviceKey={key}&numOfRows=10&pageNo=1&MobileOS=ETC&MobileApp=AppTest&_type=json&listYN=Y&arrange=C&areaCode={met_code}&sigunguCode={loc_code}&eventStartDate={date}'
            print("url :",url)
            response = requests.get(url, verify=False)
            print("response :",response)
            data=response.json()
            print(data)
            data_need=data['response']['body']['items']['item']
            print("data_need :",data_need[0]['title'])
            festival=[ 
            {"title" : data_need[i]['title'],
            "startDate" : f"{data_need[i]['eventstartdate'][:4]}/{data_need[i]['eventstartdate'][4:6]}/{data_need[i]['eventstartdate'][6:8]}",
            "endDate" : data_need[i]["eventenddate"],
            "addr1" : data_need[i]['addr1'],
            "image_small" : data_need[i]['firstimage'],
            # "image_small" : data_need[i]['firstimage2'],
            "met_code" : met_code,
            "loc_code" : loc_code
            }
            for i in range(len(data_need))
            ]
    
        except:
            festival="예정된 축제 정보가 없습니다"

        
        return festival






class fes_info:
    def fes_full(location, metro, loc):
        now = datetime.datetime.now()
        date= now.strftime("%Y")+now.strftime("%m")+now.strftime("%d")
        key = "2qOlMnHP2j9Bjvyo6tdhQNCDu9%2Bh1mm3LS9V2hXPxHfCrPW73YsGnPOrmYt1BnDjUXWywI2gOrz9c7fvwYeBHw%3D%3D"
        met_code = metro
        loc_code= loc
        print("지역코드 : ",loc_code)
        url=f'https://apis.data.go.kr/B551011/KorService/searchFestival?serviceKey={key}&numOfRows=10&pageNo=1&MobileOS=ETC&MobileApp=AppTest&_type=json&listYN=Y&arrange=C&areaCode={met_code}&sigunguCode={loc_code}&eventStartDate={date}'
        response = requests.get(url, verify=False)
        data=response.json()
        data_need=data['response']['body']['items']['item']
        festival=[
        {"title" : i['title'],
        "startDate" : i['eventstartdate'],
        "endDate" : i["eventenddate"],
        "addr1" : i['addr1'],
        "image" : i['firstimage'],
        "image_small" : i['firstimage2'],
        "mapx" : i['mapx'],
        "mapy" : i['mapy']}
        for i in data_need
        ]
        return festival



