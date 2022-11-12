
from django.urls import path
from Travel import views

urlpatterns = [
    path('', views.index),
    path('navi/', views.showNavi),
    path('movenavi/', views.movenavi),
    path('applynavi/', views.applynavi),

]
