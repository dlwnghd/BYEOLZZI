from django.shortcuts import render
from django.http import HttpRequest, JsonResponse

# Create your views here.
def join (request):
    return render(request,'join.html')