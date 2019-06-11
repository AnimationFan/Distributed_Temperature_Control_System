from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from UserDefine.ConfigReader import config_info
from 温控系统.models import User,AirC,UserRoom
from UserDefine.Controller import controller
from django.contrib import auth
from UserDefine.SessionCheck import  SessionCheck

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
            request.session["username"]=username
            search_state=UserRoom.objects.get(user_name=username)
            request.session["room"]=search_state.room
            request.session["currenttemp"]=config_info.DefaultTemp
            request.session["targettemp"]=config_info.DefaultTemp
            request.session["targetwind"]=1
            request.session["On"]="关"
            url = '/Customer/cus/' + username
            return HttpResponseRedirect(url)
        elif preuser.user_type == 'F':
            request.session["username"]=username
            return HttpResponseRedirect('/Front/')
        elif preuser.user_type == 'A':
            request.session["username"]=username
            return HttpResponseRedirect('/AirCManager/')
        elif preuser.user_type == 'H':
            request.session["username"]=username
            return HttpResponseRedirect('/HotelManager/')
    else:
      return HttpResponse('用户名或密码错误。')


def logout(request):
    del request.session["username"]  # 删除session
    return HttpResponseRedirect('/login/')


def setPassWord(request):
    username = request.GET['username']
    oldpwd = request.GET['oldpwd']
    newpwd = request.GET['newpwd']
    user = User.objects.filter(user_name=username, password=oldpwd)
    if user:
        User.objects.filter(user_name=username).update(password=newpwd)
        return HttpResponse('密码修改成功。')
    else:
        return HttpResponse('用户名或密码不正确。')

def welcome(request):
    return render(request, 'login.html')

def writesession(request):
    SessionCheck.writeSession(request,"1004","1004","C")
    return HttpResponse("写入session成功")

def readsession(request):
    result=SessionCheck.readSession(request)
    return HttpResponse(result["user_name"]+result["password"]+result["type"])

def test_decoratort(request):
    result= SessionCheck.checkSession(request)
    if result:
        return  HttpResponse("Success")
    else:
        return HttpResponse("Fail")