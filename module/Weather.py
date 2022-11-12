import requests
from bs4 import BeautifulSoup


class Weather_crawl:

    def __init__(self) -> None:
        pass

    def weather(self, location):

        # url 지정
        url = f"https://search.naver.com/search.naver?sm=tab_hty.top&where=nexearch&query={location}+날씨&oquery=%EB%82%A0%EC%94%A8&tqi=h2bHZlp0J1sssTGpvh4ssssss8C-147890"

        # 응답 확인
        response = requests.get(url)   # get 방식으로 해당 url 로 request 를 보내고 response 를 받아서 리턴함

        # dom 지정
        dom = BeautifulSoup(response.text, "html.parser")

        # 날씨 html태그
        elements = dom.select("span.weather.before_slash")
        location_weather = elements[0].text

        return location_weather

    def weather_info(self, location):
        weather_info = {}

        # url 지정
        url = f"https://search.naver.com/search.naver?sm=tab_hty.top&where=nexearch&query={location}+날씨&oquery=%EB%82%A0%EC%94%A8&tqi=h2bHZlp0J1sssTGpvh4ssssss8C-147890"

        # 응답 확인
        response = requests.get(url)   # get 방식으로 해당 url 로 request 를 보내고 response 를 받아서 리턴함

        # dom 지정
        dom = BeautifulSoup(response.text, "html.parser")

        # location 날씨
        weather_info['location_weather'] = location + " 날씨"

        # 현재 온도
        elements = dom.find("div",{"class" : "temperature_text"}).find_all(text = True)
        # elements.text.strip()
        temp_li = elements[2] + elements[3]
        
        weather_info['temp'] = elements[1]
        weather_info['temp_num'] = temp_li

        # 어제보다
        weather_info['yester'] = "어제보다"

        # 🔵🔵🔵도 높아요/낮아요 
        elements = dom.select(".temperature_info .summary .temperature")
        weather_info['yester_temp'] = elements[0].text.replace('요 ','요')

        # 체감
        weather_info['bodytemp'] = "체감"

        # 체감 html태그
        elements_desc = dom.select(".temperature_info .summary_list .desc")
        weather_info['bodytemp_num'] = elements_desc[0].text

        # 습도
        weather_info['moisture'] = "습도"

        # 습도 html태그
        weather_info['moisture_num'] = elements_desc[1].text

        # 바람
        elements = dom.select(".temperature_info .summary_list .term")
        weather_info['wind'] = elements[2].text

        # 바람 html태그
        weather_info['wind_num'] = elements_desc[2].text

        # 미세먼지 html태그
        weather_info['dust'] = "미세먼지"

        # 미세먼지 정보 html태그
        elements_txt = dom.select(".today_chart_list .item_today a .txt")
        weather_info['dust_stat'] = elements_txt[0].text

        # 초미세먼지 html태그
        weather_info['micro_dust'] = "초미세먼지"

        # 초미세먼지 정보 html태그
        weather_info['micro_dust_stat'] = elements_txt[1].text

        # 자외선 html태그
        weather_info['sun'] = "자외선"

        # 자외선 정보 html태그
        weather_info['sun_stat'] = elements_txt[2].text

        # 일출 html태그
        weather_info['sunrise'] = "일출"

        # 일출 정보 html태그
        weather_info['sunrise_time'] = elements_txt[3].text

        return weather_info