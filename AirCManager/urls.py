from django.conf.urls import url
from AirCManager import views

urlpatterns = [
    url(r'^AirCManager/TurnOn$', views.prema.TurnOn()),
    url(r'^AirCManager/TurnOff$', views.prema.turnOff()),
    url(r'^AirCManager/addAirC$', views.prema.addAirC()),     #输入房号(room)（str格式）   房号不能重复，添加失败会提示
    url(r'^AirCManager/delAirC$', views.prema.delAirC()),     #输入房号(room)（str格式）   只能删除无人居住的房间，删除失败会提示
    url(r'^AirCManager/', views.prema.welcome()),            #显示空调清单（ID、顾客号、开关与否） 函数返回清单信息
]