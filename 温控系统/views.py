from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from UserDefine.ConfigReader import config_info
from 温控系统.models import User,AirC
from UserDefine.Controller import controller
from django.contrib import auth

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


def login(request):
    username = request.POST.get('name')
    pwd = request.POST.get('password')
    user = User.objects.filter(user_name=username, password=pwd)
    if user.count()>0:
        preuser = user[0]
        if preuser.user_type == 'C':
            url = '/Customer/cus/' + username
            return HttpResponseRedirect(url)
        elif preuser.user_type == 'F':
            return HttpResponseRedirect('/Front/')
        elif preuser.user_type == 'A':
            return HttpResponseRedirect('/AirCManager/')
        elif preuser.user_type == 'H':
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
    user = User.objects.filter(user_name=username, password=oldpwd)
    if user:
        User.objects.filter(user_name=username).update(password=newpwd)
        return HttpResponse('密码修改成功。')
    else:
        return HttpResponse('用户名或密码不正确。')

def welcome(request):
    return render(request, 'login.html')