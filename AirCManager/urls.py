from django.conf.urls import url
from django.contrib import admin
from django.urls import path
from AirCManager import views

urlpatterns = [
    path('TurnOn/', views.TurnOn),
    path('TurnOff/', views.turnOff),
    path('addAirC/', views.addAirC),     #输入房号(room)（str格式）   房号不能重复，添加失败会提示
    path('delAirC/', views.delAirC),     #输入房号(room)（str格式）   只能删除无人居住的房间，删除失败会提示
    path('logout/',views.logout),
    path(r'', views.welcome)            #显示空调清单（ID、顾客号、开关与否） 函数返回清单信息（list)、添加空调操作结果(result1,result1='success'或者'error'),删除操作结果(result2,数值同result1)
]