from django.shortcuts import render
from django.http import HttpRequest

# Create your views here.
def index(request):
    return render(request, 'daemon.html')

