from django.shortcuts import render
from django.http import HttpResponse
from UserDefine.ConfigReader import config_info
from 温控系统.models import User,AirC
from UserDefine.Controller import controller

def addair(request):
    print(controller.getStates())
    print(controller.addAirC("1009"))
    print(AirC.objects.all())
    return HttpResponse('Hello')

def delair(request):
    print(AirC.objects.all())
    print(controller.delAirC("1009"))
    print(AirC.objects.all())
    return  HttpResponse('删除完成')

def show_config(request):
    print(config_info)
    for airc in AirC.objects.all():
        print(airc.room_num)
    return HttpResponse('Hello')
# Create your views here.

def init(request):
    users=User.objects.all()
    for user in users:
        print(user.user_name,user.password,user.user_type)
    aircs=AirC.objects.all()
    for airc in aircs:
        print(airc.room_num)
    return HttpResponse("初始化完成")