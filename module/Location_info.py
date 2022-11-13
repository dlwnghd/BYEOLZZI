from bs4 import BeautifulSoup
import requests

class LocationInfo:

    def __init__(self) -> None:
        pass

    def crawlingNaver(self,url):

        response = requests.get(url)   # 동적인애는 이걸로 가져올수 없음
        if response.status_code == 200:          # 에러 확인은 필수!
            dom = BeautifulSoup(response.text, "html.parser")
        title = dom.select_one('b.commonGeoInfo_name__98mqw').text
        text = dom.select_one('p.expandableText_desc__2u9cG > span.text').text
        img_list = dom.select('div.topImages_list__1SyZT > div > a > figure > img')
        img_url = [
            img.attrs["src"]
            for img in img_list
        ]
        content = {
            'title' : title,
            'text' : text,
            'img_url' : img_url,
        }
        return content
