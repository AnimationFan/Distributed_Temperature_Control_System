from django.conf.urls import url
from django.contrib import admin
from HotelManager import views

urlpatterns = [
    url(r'^HotelManager/setCharge$', views.prema.setCharge()),      # 需要计费参数(charge)
    url(r'^HotelManager/setTemp$', views.prema.setTemp()),          # 需要默认温度数值(temp)
    url(r'^HotelManager/getReport$', views.prema.getReport()),      # 生成报表,需要顾客号(customID)、房间号(roomID)  函数返回报表内容
    url(r'^HotelManager/', views.prema.welcome()),                  # 列举顾客清单（包括顾客ID、房间号）
]