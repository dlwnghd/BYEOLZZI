from bs4 import BeautifulSoup
import requests

class LocationInfo:

    def __init__(self) -> None:
        pass

    def crawlingNaver(self,url):

        response = requests.get(url)        # 동적인애는 이걸로 가져올수 없음
        if response.status_code == 200:     # 에러 확인은 필수!
            dom = BeautifulSoup(response.text, "html.parser")

        # 크롤링 정보 담기
        title = dom.select_one('b.commonGeoInfo_name__98mqw').text                      # 지역정보 타이틀
        text = dom.select_one('p.expandableText_desc__2u9cG > span.text').text          # 지역정보 설명
        img_list = dom.select('div.topImages_list__1SyZT > div > a > figure > img')     # 지역정보 이미지

        pick_link_list = dom.select('div.news_PostItem__1D8hn > a')                     # 에디터픽 링크
        pick_img_list = dom.select('div.news_PostItem__1D8hn > a > figure > img')       # 에디터픽 이미지
        pick_text_list = dom.select('div.news_PostItem__1D8hn > a > span')              # 에디터픽 설명

        hotel_link_list = dom.select('div.lodge_HotelItem__3duZP > a')                                          # 숙박업소 링크
        hotel_img_list = dom.select('div.lodge_HotelItem__3duZP > a > figure > img')                            # 숙박업소 이미지
        hotel_name_list = dom.select('div.lodge_HotelItem__3duZP > a > div > span')                             # 숙박업소 상업명
        hotel_score_list = dom.select('div.lodge_HotelItem__3duZP > a > div > div > span.lodge_rating__WQkRT')  # 숙박업소 별점

        # 지역 정보 html에서 표현하기 쉽게 가공하기
        img_url = self.for_list(img_list, "src")    # 지역 이미지 주소

        # 에디터픽 정보 html에서 표현하기 쉽게 가공하기
        pick_link_url = self.for_list(pick_link_list, "href")   # 에디터픽 url 주소
        pick_img_url = self.for_list(pick_img_list, "src")      # 에디터픽 이미지 주소
        pick_text = self.for_text_list(pick_text_list)          # 에디터픽 텍스트 정보
        result_pick_list = self.pick_list(pick_img_url, pick_link_url, pick_text) # 에디터픽 3가지 정보를 하나의 리스트로 담아주는애

        # 숙소추천 정보 html에서 표현하기 쉽게 가공하기
        hotel_link_url = self.for_list(hotel_link_list, "href")         # 숙박업소 url 주소
        hotel_img_url = self.for_list(hotel_img_list, "src")            # 숙박업소 이미지 주소
        hotel_name_text = self.for_text_list(hotel_name_list)           # 숙박업소 업소명 텍스트 정보
        hotel_score = self.for_text_list(hotel_score_list)              # 숙박업소 별점
        result_hotel_list = self.hotel_list(hotel_img_url, hotel_link_url, hotel_name_text, hotel_score)   # 호텔 6가지 정보를 하나의 리스트로 담아주는애

        # html로 가공한 리스트들 리턴해주기.
        content = {
            'title' : title,
            'text' : text,
            'img_url' : img_url,
            'result_pick_list' : result_pick_list,      # 0: img, 1: link, 2: text
            'result_hotel_list' : result_hotel_list,    # 0: img, 1: link, 2: text, 3: score, 4:money, 5:monetary
        }
        return content


    def pick_list(self, img, link, text):
        li = []

        for i in range(len(img)):
            l = []
            l.append(img[i])
            l.append(link[i])
            l.append(text[i])
            li.append(l)
        return li

    def hotel_list(self, img, link, text, score):
        li = []

        for i in range(len(img)):
            l = []
            l.append(img[i])
            l.append(link[i])
            l.append(text[i])
            l.append(score[i])
            li.append(l)
        return li

    def for_list(self, i_li, key):
        li = [
            i.attrs[key]
            for i in i_li
        ]
        return li


    def for_text_list(self, i_li):
        li = [
            i.text
            for i in i_li
        ]
        return li
