from django.shortcuts import render
from django.http import HttpResponse
from UserDefine.ConfigReader import config_info
from 温控系统.models import User,AirC


def show_config(request):
    print(config_info)
    return HttpResponse('Hello')
# Create your views here.

def login(request):
    return HttpResponse('LOGIN')
# Create your views here.

def init(request):
    users=User.objects.all()
    for user in users:
        print(user.user_name,user.password,user.user_type)
    aircs=AirC.objects.all()
    for airc in aircs:
        print(airc.room_num)
    return HttpResponse("初始化完成")