# 모듈 불러오기
from django.shortcuts import render
from django.http import HttpRequest, JsonResponse
from config.weather_crawling_LJH import weather_crawl
from BYEOLZZI.models import Answer

# Create your views here.
def index(request):
    return render(request, 'daemon.html')

def aroundShow(request:HttpRequest):
    localname = request.GET.get("localname")
    areachoice = request.GET.get("areachoice")
    addr = request.GET.get("addr")
    mapx = request.GET.get("mapx")
    mapy = request.GET.get("mapy")

    print("localname :", localname)

    context = {
        "LocalName" : localname,
        "AreaChoice" : areachoice,
        "Addr" : addr,
        "MapX" : mapx,
        "MapY" : mapy,
    }

    return render(request, 'aroundshow.html', {'data' : context})

def weather(request):
    weather_loc =  request.GET.get('Ner')
    print("weather:",weather_loc)

    context = {
        'weather' : weather_loc
    }

    return JsonResponse(context)

def weathers(request):
    weather =  request.GET.get('data')
    print("weather:",weather)

    weather_info = weather_crawl.weather(weather)
    weather_etc = weather_crawl.weather_info(weather)

    context={
        "data" : weather_info,
        "etc" : weather_etc
    }
    
    return render(request, 'weather.html', context)
