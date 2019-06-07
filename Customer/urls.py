from django.conf.urls import url
from django.urls import path
from django.contrib import admin
from Customer import views

urlpatterns = [
    path('TurnOn/', views.TurnOn),
    path('setTemp/', views.setTemp),          #温度数值(temp) 只能提交固定范围
    path('setWind/', views.setWind),          #风速数值(wind)（1、2、3）
    path('getAccount/', views.getAccount),
    path('TurnOff/', views.TurnOff),
    path('get_temp/',views.get_temp),
    path('get_On/',views.get_On),
    path('inita/',views.inita),
    path('logout/',views.logout),
    path('cus/<username>', views.welcome),                 #需要顾客号(id)   #返回房间号(room:str)、目标温度(targettemp:int)、室温(currenttemp:int)、风速(wind:int)、开关与否(On:bool)
]