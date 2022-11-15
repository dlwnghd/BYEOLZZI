from django.urls import path
from Travel import views

urlpatterns = [
    path('', views.index),
    path('navi/', views.showNavi),
    path('movenavi/', views.movenavi),
    path('applynavi/', views.applynavi),
    path('aroundshow/', views.aroundShow),
    path('highway/', views.highway),
    path('heeji/', views.heeji_iframe), # heeji iframe 띄우기
    path('festival/', views.festival),
    path('festivals/', views.festivals),
    path('weather/', views.weather),
    path('weathers/', views.weathers),
    path('location_info/', views.location_info),
    path('mylist/', views.mylist),
    path('delete_list/', views.delete_list),
    path('basepage/', views.basepage),
    path('save_location/', views.saveLocation),
    path('damgi_location/', views.damgiLocation)
]
