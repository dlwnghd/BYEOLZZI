
from django.urls import path
from Travel import views

urlpatterns = [
    path('', views.index),
    path('festival/', views.festival),
    path('festivals/', views.festivals),
]
