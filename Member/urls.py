from django.urls import path
from . import views

urlpatterns = [
    path('join/', views.join),
    path('join/idduplicate', views.idDuplicateCheck),
    path('join/create', views.createMember),
    path('login/', views.login),

]