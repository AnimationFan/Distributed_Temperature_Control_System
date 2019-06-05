from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from UserDefine.ConfigReader import config_info
from 温控系统.models import User,AirC
from django.contrib import auth



def show_config(request):
    print(config_info)
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

def login(request):
    username = request.GET['name']
    pwd = request.GET['password']
    user = User.objects.filter(user_name = username, password = pwd)
    if user:
        auth.login(request, None)

        if user.user_type == 'C':
            return HttpResponseRedirect('/Customer/')
        elif user.user_type == 'F':
            return HttpResponseRedirect('/Front/')
        elif user.user_type == 'A':
            return HttpResponseRedirect('/AirCManager/')
        elif user.user_type == 'H':
            return HttpResponseRedirect('/HotelManager/')
            
    else:
        return HttpResponse('用户名或密码错误。')

def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/login/')

def setPassWord(request):
    username = request.GET['username']
    oldpwd = request.GET['oldpwd']
    oldpwd = request.GET['newpwd']
    user = User.objects.filter(user_name = username, password = oldpwd)
    if user:
        User.objects.filter(user_name = username).update(password = newpwd)
        return HttpResponse('密码修改成功。')
    else:
        return HttpResponse('用户名或密码不正确。')
