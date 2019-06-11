from django.shortcuts import render_to_response

from django.shortcuts import render
from django.http import HttpResponseRedirect,HttpResponse
from django.contrib.auth.decorators import login_required
from UserDefine.Controller import Controller, controller
from 温控系统 import models
from UserDefine.ConfigReader import config_info, DefaultConfig
import os

# -*- coding: UTF-8 -*-


#@login_required
def welcome(request):
    session_check=request.session.get("username")
    if not session_check:
        return HttpResponseRedirect("../")
    if session_check!='1003':
        return HttpResponseRedirect("../")
    showlist=[]
    seacus=models.UserRoom.objects.all()
    for var2 in seacus:
            a = {"customer": var2.user_name, "room": var2.room}
            showlist.append(a)
    return render(request,'Front.html',{"list":showlist})


def viewlogin(request):
    session_check=request.session.get("username")
    if not session_check:
        return HttpResponseRedirect("../../")
    if session_check!='1003':
        return HttpResponseRedirect("../")
    return render(request, 'login1.html')

#@login_required
def login(request):
    session_check=request.session.get("username")
    if not session_check:
        return HttpResponseRedirect("../../")
    if session_check!='1003':
        return HttpResponseRedirect("../../")
    user = request.GET['customerId']
    pwd = request.GET['password']
    roomid = request.GET['roomId']
    if user in models.User.objects.all().values_list('user_name', flat=True):
        print(models.User.objects.all().values_list('user_name', flat=True))
        message = '用户名已存在。'
    elif roomid not in models.AirC.objects.all().values_list('room_num', flat=True):
        message = "房间不存在。"
    else:
        if models.UserRoom.objects.filter(room=roomid).count()>0:
            message = '房间已有人入住。'
        else:
            temp = models.User.objects.create(user_name= user, password = pwd, user_type = 'C')
            models.UserRoom.objects.create(user_name=user, room=roomid, schedulingtimes='0', reachtimes='0')
            message = '注册成功。'
    return HttpResponse(message)


#@login_required
def getAccount(request):
    session_check=request.session.get("username")
    if not session_check:
        return HttpResponseRedirect("../../")
    if session_check!='1003':
        return HttpResponseRedirect("../../")
    global controller
    roomid = request.GET['roomId']
    if roomid in models.AirC.objects.all().values_list('room_num', flat=True):
        if models.UserRoom.objects.filter(room = roomid).count() > 0 :
            userroom = models.UserRoom.objects.get(room=roomid)
            user_name=userroom.user_name
            record = models.UseRecord.objects.filter(room_num=roomid,  user_name=userroom.user_name)
        else:
            return HttpResponse('房间无人入住。')
        showlist=[]
        totalcost = 0.0
        for var in record:
            a={'begin_time':var.begin_time,'end_time':var.end_time,'temp':var.temp,'wind':var.wind,'cost':var.price}
            a['cost']=round(a['cost'],1)
            showlist.append(a)
            totalcost=totalcost+var.price
        length=len(record)
        if length>0:
          if showlist[length-1]['cost']==-1:
            showlist[length-1]['cost']=controller.getAccount(roomid,user_name)
        totalcost=round(totalcost,1)
    else:
        return HttpResponse('房间号不存在。')
    return render(request, 'Account.html', {'list': showlist, 'cost':totalcost})


def viewlogout(request):
    session_check=request.session.get("username")
    if not session_check:
        return HttpResponseRedirect("../../")
    if session_check!='1003':
        return HttpResponseRedirect("../../")
    return render(request, 'logout1.html')

#@login_required
def logout(request):
    session_check=request.session.get("username")
    if not session_check:
        return HttpResponseRedirect("../../")
    if session_check!='1003':
        return HttpResponseRedirect("../../")
    roomid = request.GET["roomId"]
    if roomid in models.AirC.objects.all().values_list('room_num', flat=True):
        userroom = models.UserRoom.objects.filter(room=roomid)
        if userroom:
            user = userroom[0].user_name
            userroom.delete();
            models.User.objects.filter(user_name=user).delete()
            models.UseRecord.objects.filter(user_name=user).delete()
        message = '注销成功。'
    else:
        message = '房间不存在。'
    return HttpResponse(message)

def logout2(request):
    session_check=request.session.get("username")
    if not session_check:
        return HttpResponseRedirect("../../")
    if session_check!='1003':
        return HttpResponseRedirect("../../")
    del request.session["username"]  # 删除session
    return HttpResponseRedirect('../../')

# Create your views here.
