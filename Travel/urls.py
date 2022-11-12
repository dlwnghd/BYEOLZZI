
from django.urls import path
from Travel import views
print("여행 url 옴")
urlpatterns = [
    path('', views.index),
    path('aroundshow/', views.aroundShow),
    path('weather/', views.weather),
    path('weathers/', views.weathers),
]
