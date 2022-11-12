from django.shortcuts import render
from django.http import HttpRequest, JsonResponse
from config.highway_heeji import Highway

# Create your views here.
def index(request):
    return render(request, 'daemon.html')

def highway(request):
    print('ajax views에 들어옴!!!!!!!!')
    data = request.GET.get('data')
    print('data:',  data)
    print('data type: ', type(data))

    # highway =Highway(data)
    # real_data = highway.web_full()
    # print(real_data)


    context = {
        'data' : data
    }

    return JsonResponse(context)
    # return render(request, 'heeji/highway_info.html')


def heeji_iframe(request):
    print('ajax views에 들어옴!!!!!!!!2222222222')
    data = request.GET.get('data')
    print('data:',  data)
    print('data type: ', type(data))

    highway =Highway(data)
    real_data = highway.web_full()
    print('real_data: ',real_data)

    context = {
        # 'data' : '하이?'
        'data' : data,
        'real_data' : real_data

    }

    return render(request, 'heeji/highway_info.html', context)
    # return JsonResponse(context)