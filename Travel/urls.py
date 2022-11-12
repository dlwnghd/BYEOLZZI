
from django.urls import path
from Travel import views

urlpatterns = [
    path('', views.index),
    path('highway/', views.highway),


    # heeji iframe 띄우기
    path('heeji/', views.heeji_iframe),
    
]
