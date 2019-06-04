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
    targettem=Default.DefaultTemp
    user=id

    def __init__(self):
        self.targettem=Default.DefaultTemp

precus=Customer()

@login_required
def welcome(request):
    precus.id = request.GET['id']
    pre = models.UserRoom.object.get(User_name=precus.id)
    preroom=pre.room.room_num
    precus.room=preroom
    temp=precus.targettem
    #return render_to_response('welcome.html',{'room':preroom,'temp':temp})

    #开启空调
@login_required
def TurnOn(request):
    global controller
    controller.turnOnAirC(precus.id,precus.room)
    HttpResponseRedirect("/Customer/")

    #设置温度
def setTemp(request):
    global controller
    last = controller.getStates();
    for var in last:
        if var["RoomNum"]==precus.room:
              lastone=var
    t = request.GET['temp']
    t = int(t)
    w=lastone['Temp']
    controller.setAirCState(precus.room,t,w,precus.id)
    HttpResponseRedirect("/Customer/")

    #设置风速
@login_required
def setWind(request):
    global controller
    last = controller.getStates();
    for var in last:
      if var["RoomNum"] == precus.room:
         lastone = var
    w = request.GET['wind']
    w = int(w)
    t=lastone["Temp"]
    controller.setAirCState(precus.room,t,w,precus.id)
    HttpResponseRedirect("/Customer/")

@login_required
def getAccount(request):
    global controller
    getlist=models.UseRecord.objects.filter(room_num=precus.room)
    totalcost=0.0
    for var in getlist:
      totalcost=totalcost+var.price
    totalcost=totalcost+controller.getAccount(precus.id,precus.room)
    return render_to_response('Customer.html',{'cost':totalcost})

@login_required
def turnOff(request):
   global controller
   controller.turnOnAirC(precus.id,precus.room)
   HttpResponseRedirect("/Customer/")





