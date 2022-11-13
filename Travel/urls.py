
from django.urls import path
from Travel import views

urlpatterns = [
    path('', views.index),
    path('location_info/', views.location_info),

]
