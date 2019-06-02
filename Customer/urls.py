from django.conf.urls import url
from django.contrib import admin
from Customer import views

urlpatterns = [
    url(r'^Customer/TurnOn$', views.precus.TurnOn()),
    url(r'^Customer/setTemp$', views.precus.setTemp()),          #温度数值(temp) 只能提交固定范围
    url(r'^Customer/setWind$', views.precus.setWind()),          #风速数值(wind)（1、2、3）
    url(r'^Customer/getAccount$', views.precus.getAccount()),
    url(r'^Customer/TurnOff$', views.precus.turnOff()),
    url(r'^Customer/', views.precus.welcome()),                 #需要顾客号(id)   #返回房间号
]