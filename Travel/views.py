# 모듈 불러오기
import json

from django.shortcuts import render
from django.http import HttpRequest, JsonResponse
from module.Weather import Weather_crawl
from module.Findway import Findway

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

def weather(request:HttpRequest):
    weather_loc =  request.GET.get('Ner')
    print("weather:",weather_loc)

    context = {
        'weather' : weather_loc
    }

    return JsonResponse(context)

def weathers(request:HttpRequest):
    weather =  request.GET.get('data')
    print("weather:",weather)

    wc = Weather_crawl()

    weather_info = wc.weather(weather)
    weather_etc = wc.weather_info(weather)

    context={
        "data" : weather_info,
        "etc" : weather_etc
    }
    
    return render(request, 'weather.html', context)

def showNavi(request):
    print("Ajax 들어옴 showNavi")
    nerlist = json.loads(request.GET.get("findway_list"))
    print("type(nerlist) : ", type(nerlist))
    print(nerlist)

    if len(nerlist) == 2:
        fw = Findway()
        loc_dict = fw.findTwoloc(nerlist[0], nerlist[1])

        context = {
            'startlat' : loc_dict['start'][0],
            'startlong' : loc_dict['start'][1],
            'endlat' : loc_dict['end'][0],
            'endlong' : loc_dict['end'][1],
        }
    else:
        fw = Findway()
        loc_tuple = fw.findOneloc(nerlist[0])
        context = {
            'startlat' : loc_tuple[0],
            'startlong' : loc_tuple[1],
        }
    
    return JsonResponse(context)
    


def movenavi(request:HttpRequest):
    startlat = request.GET.get('startlat')
    startlong = request.GET.get('startlong')
    endlat = request.GET.get('endlat')
    endlong = request.GET.get('endlong')
    print("startlat: ", startlat, "type: ", type(startlat))
    context = {
        "startlat" : startlat,
        "startlong" : startlong,
        "endlat" : endlat,
        "endlong" : endlong,
    }

    return JsonResponse(context)
    # return render(request, 'tmapnavi.html', {'data': context})

    # return render(request, 'tmapnavi.html')


def applynavi(request:HttpRequest):
    startlat = request.GET.get('startlat')
    startlong = request.GET.get('startlong')
    endlat = request.GET.get('endlat')
    endlong = request.GET.get('endlong')
    # test = request.GET.get("data")
    # print("test: ", test, "type: ", type(test))
    # test = json.loads(test)
    # print("test: ", test, "type: ", type(test))

    # print(test['a']['b'])


    print("startlat: ", startlat, "type: ", type(startlat))
    context = {
        "startlat" : startlat,
        "startlong" : startlong,
        "endlat" : endlat,
        "endlong" : endlong,
        # "test": test
    }
    return render(request, 'tmapnavi.html', {'data': context})
