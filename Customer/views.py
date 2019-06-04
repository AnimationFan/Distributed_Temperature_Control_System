from django.shortcuts import render_to_response

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect

from UserDefine.Controller import Controller,controller

from 温控系统 import models
from UserDefine.ConfigReader import config_info,DefaultConfig

# -*- coding: UTF-8 -*-

Default=DefaultConfig()


class Customer:
    id=''
    room=''
    targettemp=Default.DefaultTemp
    targetwind=1
    user=id

    def __init__(self):
        self.targettemp=Default.DefaultTemp

precus=Customer()

@login_required
def welcome(request):
    precus.id = request.GET['id']
    pre = models.UserRoom.object.get(User_name=precus.id)
    preroom=pre.room.room_num
    precus.room=preroom
    last = controller.getStates();
    for var in last:
        if var["RoomNum"]==precus.room:
              lastone=var
    currenttemp=lastone['Temp']
    return render_to_response('welcome.html',{'room':preroom,'targettemp':precus.targettemp,'currenttemp':currenttemp,'targetwind':precus.targetwind})

    #开启空调
@login_required
def TurnOn(request):
    global controller
    controller.turnOnAirC(precus.id,precus.room)
    HttpResponseRedirect("/Customer/")

    #设置温度
def setTemp(request):
    global controller
    t = request.GET['temp']
    t = int(t)
    precus.targettemp = t
    w=precus.targetwind
    controller.setAirCState(precus.room,t,w,precus.id)
    HttpResponseRedirect("/Customer/")

    #设置风速
@login_required
def setWind(request):
    global controller
    w = request.GET['wind']
    w = int(w)
    precus.targetwind = w
    t=precus.targettemp
    controller.setAirCState(precus.room,t,w,precus.id)
    HttpResponseRedirect("/Customer/")

@login_required
def getAccount(request):
    global controller
    getlist=models.UseRecord.objects.filter(room_num=precus.room)
    totalcost=0.0
    for var in getlist:
      totalcost=totalcost+var.price
    totalcost=totalcost+controller.getAccount(precus.room,precus.id)
    return render_to_response('Customer.html',{'cost':totalcost})

@login_required
def turnOff(request):
   global controller
   controller.turnOnAirC(precus.id,precus.room)
   HttpResponseRedirect("/Customer/")





