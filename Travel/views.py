import json

from django.shortcuts import render
from django.http import HttpRequest, JsonResponse

from config.State import State
from BYEOLZZI.models import Members, MemberLocation
from Member.views import join

from module.Findway import Findway
from module.highway_heeji import Highway
from module.festival import fes_info
from module.Weather import Weather_crawl
from module.Location_info import LocationInfo

# Create your views here.


def index(request):
    return render(request, 'daemon.html')

# 길찾기


def showNavi(request):
    print("Ajax 들어옴 showNavi")
    nerlist = json.loads(request.GET.get("findway_list"))
    print("type(nerlist) : ", type(nerlist))
    print(nerlist)

    if len(nerlist) == 2:
        fw = Findway()
        loc_dict = fw.findTwoloc(nerlist[0], nerlist[1])

        context = {
            'startlat': loc_dict['start'][0],
            'startlong': loc_dict['start'][1],
            'endlat': loc_dict['end'][0],
            'endlong': loc_dict['end'][1],
        }
    else:
        fw = Findway()
        loc_tuple = fw.findOneloc(nerlist[0])
        context = {
            'startlat': loc_tuple[0],
            'startlong': loc_tuple[1],
        }

    return JsonResponse(context)


def movenavi(request):
    startlat = request.GET.get('startlat')
    startlong = request.GET.get('startlong')
    endlat = request.GET.get('endlat')
    endlong = request.GET.get('endlong')
    print("startlat: ", startlat, "type: ", type(startlat))
    context = {
        "startlat": startlat,
        "startlong": startlong,
        "endlat": endlat,
        "endlong": endlong,
    }

    return JsonResponse(context)


def applynavi(request):
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
        "startlat": startlat,
        "startlong": startlong,
        "endlat": endlat,
        "endlong": endlong,
        # "test": test
    }
    return render(request, 'tmapnavi.html', {'data': context})


# 주변검색
def aroundShow(request: HttpRequest):
    localname = request.GET.get("localname")
    areachoice = request.GET.get("areachoice")
    addr = request.GET.get("addr")
    mapx = request.GET.get("mapx")
    mapy = request.GET.get("mapy")

    print("localname :", localname)

    context = {
        "LocalName": localname,
        "AreaChoice": areachoice,
        "Addr": addr,
        "MapX": mapx,
        "MapY": mapy,
    }

    return render(request, 'aroundshow.html', {'data': context})


# 교통현황
def highway(request):
    print('ajax views에 들어옴!!!!!!!!')
    data = request.GET.get('data')
    print('data:',  data)
    print('data type: ', type(data))

    # highway =Highway(data)
    # real_data = highway.web_full()
    # print(real_data)

    context = {
        'data': data
    }

    return JsonResponse(context)


def heeji_iframe(request):
    print('ajax views에 들어옴!!!!!!!!2222222222')
    data = request.GET.get('data')
    print('data:',  data)
    print('data type: ', type(data))

    highway = Highway(data)
    real_data = highway.web_full()
    print('real_data: ', real_data)

    context = {
        # 'data' : '하이?'
        'data': data,
        'real_data': real_data

    }

    return render(request, 'heeji/highway_info.html', context)


# 축제
def festival(request):
    print('너 들어왔니??? 좀 들어와라')
    data = request.GET.get('ner')
    met_code = request.GET.get('met_code')
    loc_code = request.GET.get('loc_code')
    print("이게 뭐야 :", data)
    print("메트로 :", met_code)
    print("지역 :", loc_code)

    context = {
        "ner": data,
        "met_code": met_code,
        "loc_code": loc_code
    }
    return JsonResponse(context)


def festivals(request):
    print('두 번째꺼 들어옴')
    ner = request.GET.get('ner')
    met_code = request.GET.get('met_code')
    loc_code = request.GET.get('loc_code')
    print('data : ', ner)
    print("met :", met_code)
    print("loc_code :", loc_code)
    festi = fes_info.fes_full(ner, met_code, loc_code)
    print(festi)

    context = {
        "ner": ner,
        "data": festi
    }

    return render(request, 'festival_jbs.html', context)


# 날씨
def weather(request: HttpRequest):
    weather_loc = request.GET.get('Ner')
    print("weather:", weather_loc)

    context = {
        'weather': weather_loc
    }

    return JsonResponse(context)


def weathers(request: HttpRequest):
    weather = request.GET.get('data')
    print("weather:", weather)

    wc = Weather_crawl()

    weather_info = wc.weather(weather)
    weather_etc = wc.weather_info(weather)

    context = {
        "data": weather_info,
        "etc": weather_etc
    }

    return render(request, 'weather.html', context)


# 여행지 정보
def location_info(request):         # 여행지정보용 함수

    url = request.GET.get("url")            # 크롤링 url 받음.

    location = LocationInfo()               # 크롤링할 클레스 가져옴
    context = location.crawlingNaver(url)   # 크롤링 하는애

    # iframe 으로 context에 담아서 보냄
    return render(request, 'location_info.html', context)

# 리스트 불러오기


def mylist(request: HttpRequest):
    try:
        user_idx = request.session['login']
    except:
        print("로그인이 안되어있어!")
        return render(request, 'join.html')

    my_loca_list = {}

    member = Members.objects.get(members_idx=user_idx)
    ml_list = MemberLocation.objects.filter(m_idx=member).values("ml_idx", "m_idx", "location_list")

    for i, dic in enumerate(ml_list):
        my_loca_list[i] = dic
    print(my_loca_list)

    context = {
        'my_loca_list': my_loca_list
    }
    return JsonResponse(context)


def delete_list(request: HttpRequest):
    try:
        ner = request.GET.get('Ner')

        user_idx = request.session['login']

        member = Members.objects.get(members_idx=user_idx)
        delete_obj = MemberLocation.objects.get(
            m_idx=member, location_list=ner)
        delete_obj.delete()
        context = {
            'success': 'ok'
        }
    except:
        context = {
            'success': 'no'
        }
    return JsonResponse(context)


def basepage(request):
    query = request.GET.get("query")

    context = {
        "query": query,
    }
    return render(request, 'basepage.html', context)


def saveLocation(request: HttpRequest):
    user_idx = request.session['login']
    save_loca = request.GET.get("data")
    print("save_loca:", save_loca)

    member = Members.objects.get(members_idx=user_idx)

    member.m_location = save_loca

    Members.save(member)

    context = {
        "result": save_loca
    }

    return JsonResponse(context)


def damgiLocation(request: HttpRequest):
    user_idx = request.session['login']
    damgi_loca = request.GET.get("data")
    print("damgi_loca:", damgi_loca)
    comment = None

    member = Members.objects.get(members_idx=user_idx)
    print("member:", member)

    try:
        MemberLocation.objects.get(m_idx=member, location_list=damgi_loca)
        comment = f"{damgi_loca}은(는) 이미 저장된 여행지야! 😥"
    except Exception as e:
        print("e:", e)
        try:
            MemberLocation.objects.create(
                m_idx=member,
                location_list=damgi_loca
            )
            comment = f"{damgi_loca} 좋지! 잘 추가됐어 😉"
        except Exception as ex:
            print("ex:", ex)

    context = {
        "result": damgi_loca,
        "comment": comment
    }

    return JsonResponse(context)
