
from django.urls import path
from Travel import views

urlpatterns = [
    path('', views.index),
    path('weather/', views.weather),
    path('weathers/', views.weathers),
]
