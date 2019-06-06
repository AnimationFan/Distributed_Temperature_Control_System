from django.shortcuts import render_to_response
from django.shortcuts import render

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
    precus.id=str(precus.id)
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
    return render(request,'Customer.html',{'ID':precus.id,'On':precus.On,'targettemp':precus.targettemp,'currenttemp':precus.currenttemp,'targetwind':precus.targetwind})

    #开启空调
#@login_required
def TurnOn(request):
    global controller
    controller.turnOnAirC(precus.id,precus.room)
    url = '/Customer/cus/' + precus.id
    return HttpResponseRedirect(url)

    #设置温度
def setTemp(request):
    global controller
    t = request.POST.get('temp')
    if t=='':
        return HttpResponse('温度输入错误')
    t = int(t)
    mode = request.POST.get('mode')
    if mode=="tohot":
        if t>36 or t<21:
         return HttpResponse('制热模式温度输入错误')
    if mode=="tocold":
        if t>31 or t<16:
         return HttpResponse('制冷模式温度输入错误')
    precus.targettemp = t
    w=precus.targetwind
    controller.setAirCState(precus.room,t,w,precus.id)
    url = '/Customer/cus/' + precus.id
    return HttpResponseRedirect(url)

    #设置风速
#@login_required
def setWind(request):
    global controller
    w = request.POST.get('wind')
    if w=='':
        return HttpResponse('风速输入错误')
    w = int(w)
    precus.targetwind = w
    t=precus.targettemp
    controller.setAirCState(precus.room,t,w,precus.id)
    url = '/Customer/cus/' + precus.id
    return HttpResponseRedirect(url)

#@login_required
def getAccount(request):
    global controller
    getlist=models.UseRecord.objects.filter(room_num=precus.room)
    totalcost=0.0
    for var in getlist:
      totalcost=totalcost+var.price
    totalcost=totalcost+controller.getAccount(precus.room,precus.id)
    totalcost=str(totalcost)
    return HttpResponse(totalcost)
    #return render_to_response('Account.html',{'cost':totalcost})

#@login_required
def TurnOff(request):
   global controller
   controller.turnOffAirC(precus.id,precus.room)
   url = '/Customer/cus/' + precus.id
   return HttpResponseRedirect(url)





