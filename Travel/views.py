import json

from django.shortcuts import render
from django.http import HttpRequest, JsonResponse
from utils.Location_info import LocationInfo



# Create your views here.
def index(request):
    return render(request, 'daemon.html')

def location_info(request):         # 여행지정보용 함수
    
    url = request.GET.get("url")            # 크롤링 url 받음.

    location = LocationInfo()               # 크롤링할 클레스 가져옴
    context = location.crawlingNaver(url)   # 크롤링 하는애   

    return render(request, 'location_info.html', context)   # iframe 으로 context에 담아서 보냄


    