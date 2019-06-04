from django.shortcuts import render_to_response

from UserDefine.Controller import Controller,controller
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from 温控系统 import models
from UserDefine.ConfigReader import config_info,DefaultConfig

# -*- coding: UTF-8 -*-

class AirCManager:

    p1=1
    p2=1

    def __init__(self):
        self.p1=1
        self.p2=1

prema=AirCManager()

@login_required
def welcome(request):
    global controller,prema
    if prema.p1==1:
        result1='success'
    else:
        result1='error'
        prema.p1=0
    if prema.p2==1:
        result2='success'
    else:
        result2='error'
        prema.p2=0
    givelist=[]
    getlist = controller.getStates()
    for var in getlist:
      a={"customer":var.user_name,"room":var.room,"on":"关"}
      if var["On"]==True:
        a["on"]="开"
      givelist.append(a)
    return render_to_response('welcome.html',{'list':givelist,'result1':result1,'result2':result2})

    #开启中央空调
@login_required
def TurnOn(request):
    global controller,prema
    getlist=models.UserRoom.objects.all()
    for var in getlist:
        controller.turnOnAirC(var.user_name,var.room)
    return HttpResponseRedirect("/AirCManager/")

@login_required
def turnOff(request):
    global controller,prema
    getlist=models.UserRoom.objects.all()
    for var in getlist:
        controller.turnOffAirC(var.user_name,var.room)
    return HttpResponseRedirect("/AirCManager/")

@login_required
def delAirC(request):
    global controller,prema
    id=request.GET['room']
    result='success'
    search1=models.AirC.objects.filter(user=id)
    if search1.count()==0:
        prema.p2=0
    else:
        search2=models.UserRoom.objects.filter(user_name=id)
        if search2.count()>0:
            prema.p2=0
        else:
            models.AirC.objects.filter(user='id').delete()
    return HttpResponseRedirect("/AirCManager/")

@login_required
def addAirC(request):
    global controller,prema
    id = request.GET['room']
    prema.p1 = 'success'
    search1 = models.AirC.objects.filter(user=id)
    if search1.count()>0:
        prema.p1=0
    else:
        models.AirC.objects.create(room_num=id)
    return HttpResponseRedirect("/AirCManager/")

