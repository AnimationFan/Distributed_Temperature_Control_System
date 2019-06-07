from django.shortcuts import render_to_response

from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from UserDefine.Controller import Controller, controller
from 温控系统 import models
from UserDefine.ConfigReader import config_info, DefaultConfig
import os

# -*- coding: UTF-8 -*-


#@login_required
def welcome(request):

    showlist=[]
    seacus=models.UserRoom.objects.all()
    for var2 in seacus:
            a = {"customer": var2.user_name, "room": var2.room}
            showlist.append(a)
    return render(request,'Front.html',{"list":showlist})

def viewlogin(request):
    return render(request, 'login1.html')

#@login_required
def login(request):
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
    global controller
    roomid = request.GET['roomId']
    if roomid in models.AirC.objects.all().values_list('room_num', flat=True):
        if models.UserRoom.objects.filter(room = roomid).count() > 0 :
            userroom = models.UserRoom.objects.get(room=roomid)
            record = models.UseRecord.objects.filter(room_num=roomid,  user_name=userroom.user_name)
        else:
            return HttpResponse('房间无人入住。')

        totalcost = 0.0
        for var in record:
            totalcost += var.price
        totalcost += controller.getAccount(roomid, userroom.user_name)
    else:
        return HttpResponse('房间号不存在。')
    return render(request, 'Account.html', {'list': record, 'cost':totalcost})

def viewlogout(request):
    return render(request, 'logout1.html')

#@login_required
def logout(request):
    roomid = request.GET["roomId"]
    if roomid in models.AirC.objects.all().values_list('room_num', flat=True):
        userroom = models.UserRoom.objects.filter(room=roomid)
        if userroom:
            user = userroom[0].user_name
            userroom.delete();
            models.User.objects.filter(user_name=user).delete()
        message = '注销成功。'
    else:
        message = '房间不存在。'
    return HttpResponse(message)


# Create your views here.
