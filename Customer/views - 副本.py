from django.shortcuts import render_to_response
from django.shortcuts import render

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect,HttpResponse

from UserDefine.Controller import Controller,controller

from 温控系统 import models
from UserDefine.ConfigReader import config_info,DefaultConfig

# -*- coding: UTF-8 -*-

Default=config_info

class Customer:
    id=''
    room=''
    targettemp=Default.DefaultTemp
    currenttemp=Default.DefaultTemp
    targetwind=1
    On="关"

    def __init__(self):
        self.targettemp=Default.DefaultTemp

precus=Customer()

def init_session(request):           #重新取出session中的值
        precus.id=request.session.get("username")
        precus.room=request.session.get("room")
        precus.On=request.session.get("On")
        precus.currenttemp = request.session.get("currenttemp")
        precus.targettemp = request.session.get("targettemp")
        precus.targetwind = request.session.get("targetwind")

def change_session(request):         #修改session中的值
        pre_state_list=controller.getStates()
        for var in pre_state_list:
            if var["RoomNum"]==request.session.get("room"):
                pre_state=var
        if pre_state["On"]==True:
            request.session["On"] = "开"
        if pre_state["On"]==False:
            request.session["On"] = "关"
        request.session["currenttemp"]=pre_state["Temp"]
        request.session["targetwind"]=pre_state["Wind"]

#@login_required
def inita(request):
    models.UserRoom.objects.create(user_name="1004",room="1001")
    return HttpResponse('success')

#@login_required
def welcome(request,username):
    session_check=request.session.get("username")
    if session_check:
        init_session(request)
    else:
        return HttpResponseRedirect("../../")
    precus.id = username
    precus.id=str(precus.id)
    pre = models.UserRoom.objects.get(user_name=username)
    preroom=pre.room
    precus.room=preroom
    last = controller.getStates();
    for var in last:
        if var["RoomNum"]==precus.room:
              lastone=var
    precus.currenttemp=lastone['Temp']
    precus.currenttemp=round(precus.currenttemp,1)
    precus.On=lastone['On']
    if precus.On==True:
        precus.On="开"
    else:
        precus.On="关"
    change_session(request)
    return render(request,'Customer.html',
                  {'ID':precus.id,'On':precus.On,'targettemp':precus.targettemp,
                   'currenttemp':precus.currenttemp,'targetwind':precus.targetwind,
                   'modle':config_info.DefaultModle,'max_in_cold':config_info.ColdMaxTemp,
                   'min_in_cold':config_info.ColdMinTemp,'max_in_hot':config_info.HotMaxTemp,
                   'min_in_hot':config_info.HotMinTemp})

    #开启空调

def TurnOn(request):
    session_check=request.session.get("username")
    if session_check:
        init_session(request)
    else:
        return HttpResponseRedirect("../../")
    global controller
    controller.turnOnAirC(precus.id,precus.room)
    url = '/Customer/cus/' + precus.id
    change_session(request)
    return HttpResponseRedirect(url)

    #设置温度
def setTemp(request):
    session_check=request.session.get("username")
    if session_check:
        init_session(request)
    else:
        return HttpResponseRedirect("../../")
    global controller
    t = request.POST.get('temp')
    if t=='':
        return HttpResponse('温度输入错误')
    t = int(t)
    mode = request.POST.get('mode')
    if mode=="tohot":
        if t>30 or t<26:
         return HttpResponse('制热模式温度输入错误')
    if mode=="tocold":
        if t>26 or t<18:
         return HttpResponse('制冷模式温度输入错误')
    precus.targettemp = t
    request.session["targettemp"]=t
    w=precus.targetwind
    controller.setAirCState(precus.room,t,w,precus.id)
    url = '/Customer/cus/' + precus.id
    change_session(request)
    return HttpResponseRedirect(url)

    #设置风速
#@login_required
def setWind(request):
    session_check=request.session.get("username")
    if session_check:
        init_session(request)
    else:
        return HttpResponseRedirect("../../")
    global controller
    w = request.POST.get('wind')
    if w=='':
        return HttpResponse('风速输入错误')
    w = int(w)
    precus.targetwind = w
    t=precus.targettemp
    controller.setAirCState(precus.room,t,w,precus.id)
    url = '/Customer/cus/' + precus.id
    change_session(request)
    return HttpResponseRedirect(url)

#@login_required
def getAccount(request):
    session_check=request.session.get("username")
    if session_check:
        init_session(request)
    else:
        return HttpResponseRedirect("../../")
    global controller,precus
    getlist=models.UseRecord.objects.filter(user_name=precus.id,room_num=precus.room)
    totalcost=0.0
    for var in getlist:
      totalcost=totalcost+var.price
    totalcost=totalcost+controller.getAccount(precus.room,precus.id)
    if controller.getAccount(precus.room,precus.id)==-1:
        totalcost=totalcost+1
    totalcost=round(totalcost,1)
    totalcost=str(totalcost)
    change_session(request)
    return render_to_response('customer_account.html',{'customer':precus.id,'room':precus.room,'cost':totalcost})

#@login_required
def TurnOff(request):
    session_check = request.session.get("username")
    if session_check:
        init_session(request)
    else:
        return HttpResponseRedirect("../../")
    result=controller.turnOffAirC(precus.id,precus.room)
    url = '/Customer/cus/' + precus.id
    change_session(request)
    return HttpResponseRedirect(url)



def get_temp(request):
    session_check=request.session.get("username")
    if session_check:
        init_session(request)
    else:
        return HttpResponseRedirect("../../")
    last = controller.getStates();
    for var in last:
        if var["RoomNum"] == precus.room:
            lastone = var
    precus.currenttemp = lastone['Temp']
    precus.currenttemp = round(precus.currenttemp, 1)
    precus.On = lastone['On']
    if precus.On == True:
        precus.On = "开"
    else:
        precus.On = "关"

    if request.method=='get':
        currenttemp=request.GET('currenttemp')
    currenttemp=precus.currenttemp
    currenttemp=str(currenttemp)
    change_session(request)
    return HttpResponse(currenttemp)

def get_On(request):
    session_check=request.session.get("username")
    if session_check:
        init_session(request)
    else:
        return HttpResponseRedirect("../../")
    global precus
    if request.method=='get':
        currenttemp=request.GET('On')
    On=precus.On
    change_session(request)
    return HttpResponse(On)

def logout(request):
    session_check=request.session.get("username")
    if session_check:
        init_session(request)
    else:
        return HttpResponseRedirect("../../")
    del request.session["username"]  # 删除session
    del request.session["room"]
    del request.session["currenttemp"]
    del request.session["targettemp"]
    del request.session["targetwind"]
    del request.session["On"]
    return HttpResponseRedirect('../../')


