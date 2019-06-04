from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from UserDefine.Controller import Controller, controller
from 温控系统 import models
from UserDefine.ConfigReader import config_info, DefaultConfig

# -*- coding: UTF-8 -*-


class Front:
    
    @login_required
    def welcome(self):
        pass

    @login_required
    def login(self, request):
        user = request.GET['customerId']
        pwd = request.GET['password']
        roomid = request.GET['roomId']
        if user in models.User.objects.all().values_list('user_name'):
            message = '用户名已存在。'
        elif roomid not in models.AirC.objects.all().values_list('room_num'):
            message = "房间不存在。"
        else:
            models.User.objects.create(user_name = user, password = pwd, user_type = 'C')
            models.UserRoom.objects.create(user_name = user, room = roomid, schedulingtimes = '0')
            message = '注册成功。'
        return HttpResponse(message)

    @login_required
    def getAccount(self, request):
        global controller
        roomid = request.GET['roomId']
        temp = models.UserRoom.objects.filter(room=roomid)
        user = temp.user_name
        record = models.UseRecord.objects.filter(room_num = roomid)
        totalcost = 0.0
        
        for var in record:
            totalcost += var.price
        totalcost += controller.getAccount(roomid, user)

        return render(request, 'Front.html', {'list':record, 'cost':totalcost})

    @login_required
    def logout(self, request):
        roomid = request.GET['roomId']
        temp = models.UserRoom.objects.filter(room = roomid)
        user = temp.user_name
        if room not in models.AirC.objects.all().values_list('room_num'):
            message = "房间不存在。"
        else:
            models.UserRoom.objects.filter(room = roomid).delete()
            models.User.objects.filter(user_name = user).delete()
            message = '注销成功。'
        return HttpResponse(message)


# Create your views here.
