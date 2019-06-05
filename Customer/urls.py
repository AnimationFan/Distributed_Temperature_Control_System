from django.conf.urls import url
from django.contrib import admin
from Customer import views

urlpatterns = [
    url('TurnOn/', views.TurnOn),
    url('setTemp/', views.setTemp),          #温度数值(temp) 只能提交固定范围
    url('setWind/', views.setWind),          #风速数值(wind)（1、2、3）
    url('getAccount/', views.getAccount),
    url('TurnOff/', views.turnOff),
    url(r'', views.welcome),                 #需要顾客号(id)   #返回房间号(room:str)、目标温度(targettemp:int)、室温(currenttemp:int)、风速(wind:int)、开关与否(On:bool)
]