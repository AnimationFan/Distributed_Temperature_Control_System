from django.conf.urls import url
from django.contrib import admin
from Customer import views

urlpatterns = [
    url(r'^HotelManager/setCharge$', views.prema.TurnOn()),
    url(r'^HotelManager/setTemp$', views.prema.setTemp()),          #温度数值
    url(r'^HotelManager/', views.prema.welcome()),
]