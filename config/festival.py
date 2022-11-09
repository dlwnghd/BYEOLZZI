import requests
import datetime
class festival:
    def fes_sum(location):
        now = datetime.datetime.now()
        key = "2qOlMnHP2j9Bjvyo6tdhQNCDu9%2Bh1mm3LS9V2hXPxHfCrPW73YsGnPOrmYt1BnDjUXWywI2gOrz9c7fvwYeBHw%3D%3D"
        sql = sql + " where location ='{}'".format(location)
        met_code = sql['metro_code']
        loc_code= sql['metro_code']
        date=int(now.strftime("%y")+now.strftime("%m")+now.strftime("%d"))
        url=f'https://apis.data.go.kr/B551011/KorService/searchFestival?serviceKey={key}&numOfRows=10&pageNo=1&MobileOS=ETC&MobileApp=AppTest&_type=json&listYN=Y&arrange=C&areaCode={met_code}&sigunguCode={loc_code}&eventStartDate={date}'
        response = requests.get(url, verify=False)
        data=response.json()
        data_need=data['response']['body']['items']['item']
        fes_short=[
        {"title" : i['title'],
        "startDate" : i['eventstartdate'],
        "endDate" : i["eventenddate"],
        "addr1" : i['addr1'],
        "image_small" : i['firstimage2']}
        for i in data_need
        ]
        return fes_short


    def bot_search(date, location):
        key = "2qOlMnHP2j9Bjvyo6tdhQNCDu9%2Bh1mm3LS9V2hXPxHfCrPW73YsGnPOrmYt1BnDjUXWywI2gOrz9c7fvwYeBHw%3D%3D"
        sql = sql + " where location ='{}'".format(location)
        met_code = sql['metro_code']
        loc_code= sql['metro_code']
        date
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