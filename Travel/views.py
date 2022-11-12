from django.shortcuts import render
from django.http import HttpRequest, JsonResponse

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
    

