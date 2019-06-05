from django.shortcuts import render_to_response

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect,HttpResponse

from UserDefine.Controller import Controller,controller

from 温控系统 import models
from UserDefine.ConfigReader import config_info,DefaultConfig

# -*- coding: UTF-8 -*-

Default=DefaultConfig()


class Customer:
    id=''
    room=''
    targettemp=Default.DefaultTemp
    currenttemp=Default.DefaultTemp
    targetwind=1
    user=id
    On=False

    def __init__(self):
        self.targettemp=Default.DefaultTemp

precus=Customer()

#@login_required
def inita(request):
    user=models.User.objects.get(user_name="1004")
    room=models.AirC.objects.get(room_num="1001")
    models.UserRoom.objects.create(user_name=user,room=room)
    return HttpResponse('success')

#@login_required
def welcome(request,username):
    precus.id = username
    seacus=models.User.objects.get(user_name=username)
    pre = models.UserRoom.objects.get(user_name=seacus)
    preroom=pre.room.room_num
    precus.room=preroom
    last = controller.getStates();
    for var in last:
        if var["RoomNum"]==precus.room:
              lastone=var
    precus.currenttemp=lastone['Temp']
    precus.On=lastone['On']
    if precus.On==True:
        precus.On="开"
    else:
        precus.On="关"
    return render_to_response('Customer.html',{'room':precus.room,'On':precus.On,'targettemp':precus.targettemp,'currenttemp':precus.currenttemp,'targetwind':precus.targetwind})

    #开启空调
#@login_required
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
#@login_required
def setWind(request):
    global controller
    w = request.GET['wind']
    w = int(w)
    precus.targetwind = w
    t=precus.targettemp
    controller.setAirCState(precus.room,t,w,precus.id)
    HttpResponseRedirect("/Customer/")

#@login_required
def getAccount(request):
    global controller
    getlist=models.UseRecord.objects.filter(room_num=precus.room)
    totalcost=0.0
    for var in getlist:
      totalcost=totalcost+var.price
    totalcost=totalcost+controller.getAccount(precus.room,precus.id)
    return render_to_response('Account.html',{'cost':totalcost})

#@login_required
def turnOff(request):
   global controller
   controller.turnOnAirC(precus.id,precus.room)
   HttpResponseRedirect("/Customer/")





