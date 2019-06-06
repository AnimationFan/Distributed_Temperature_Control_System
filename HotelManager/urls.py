from django.conf.urls import url
from django.contrib import admin
from HotelManager import views

urlpatterns = [
    url('setCharge$', views.setCharge),      # 需要计费参数(charge)
    url('setTemp$', views.setTemp),          # 需要默认温度数值(temp)
    url('getReport$', views.getReport),      # 生成报表页面,需要顾客号(customID)、房间号(roomID)  函数返回报表内容，有str格式，有int格式
    url(r'', views.welcome),                  # 列举顾客清单（包括顾客ID、房间号）
]