from django.shortcuts import render
from django.http import HttpRequest,JsonResponse
from config.festival import fes_info


# Create your views here.
def index(request):
    return render(request, 'daemon.html')

def festival(request):
    print('너 들어왔니??? 좀 들어와라')
    data =  request.GET.get('ner')
    met_code =  request.GET.get('met_code')
    loc_code = request.GET.get('loc_code')
    print("이게 뭐야 :",data)
    print("메트로 :",met_code)
    print("지역 :",loc_code)

    context={
        "ner" : data,
        "met_code" : met_code,
        "loc_code" : loc_code
    }
    return JsonResponse(context)


def festivals(request):
    print('두 번째꺼 들어옴')
    ner =  request.GET.get('ner')
    met_code =  request.GET.get('met_code')
    loc_code = request.GET.get('loc_code')
    print('data : ', ner)
    print("met :", met_code)
    print("loc_code :", loc_code)
    festi = fes_info.fes_full(ner,met_code,loc_code)
    print(festi)

    context={
        "ner" : ner,
        "data" : festi
    }
    
    return render(request, 'festival_jbs.html', context)

