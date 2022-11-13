import requests
from bs4 import BeautifulSoup
import json


class Findway:

    def __init__(self) -> None:
        pass
    

    # github에서 좌표값을 가지고오는 메소드를 만든다.
    def findTwoloc(self, location1=None, location2=None):
        url = 'https://gist.githubusercontent.com/pjt3591oo/efaa02ff73538dd2f51f6caae939f836/raw/84c0bbdcfc0ef96f6841bd5670835beb4756dae6/sigungu.json'
        response = requests.get(url)
        response.text
        obj = json.loads(response.text)
        
        # 시작부분과 끝부분을 가지고 온다.
        start = location1
        end = location2
        lat = []
        long = []

        for k,v in obj.items():

            if start in k:
                lat.append(v['lat'])
                long.append(v['long'])
                
            if end in k:
                lat.append(v['lat'])
                long.append(v['long'])
        
        loc_list = []
        loc_dict = {}
        
        for i in list(zip(lat, long)):
            loc_list.append(i)
            
        loc_dict['start'] = loc_list[0]
        loc_dict['end'] = loc_list[1]

        return loc_dict
    
    
    def findOneloc(self, location=None):
        url = 'https://gist.githubusercontent.com/pjt3591oo/efaa02ff73538dd2f51f6caae939f836/raw/84c0bbdcfc0ef96f6841bd5670835beb4756dae6/sigungu.json'
        response = requests.get(url)
        response.text
        obj = json.loads(response.text)
        
        # 시작부분과 끝부분을 가지고 온다.
        start = location
        lat = []
        long = []

        for k,v in obj.items():

            if start in k:
                lat.append(v['lat'])
                long.append(v['long'])         

        return (lat[0], long[0])