from django.shortcuts import render_to_response
from django.shortcuts import render
from UserDefine.Controller import Controller, controller
import UserDefine.Controller
from django.http import HttpResponseRedirect,HttpResponse
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


#@login_required
def welcome(request):
    session_check=request.session.get("username")
    if not session_check:
        return HttpResponseRedirect("../")
    global prema
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
    airc_info_list=[]
    if controller.on!=False:
        airc_info_list = controller.getStates()
        for airc_info in airc_info_list:
            if airc_info["On"]=='True':
                airc_info["On"]="开"
            else:
                airc_info["On"]="关"
            if airc_info["Wind"]==0:
                airc_info["Wind"]=""
            if airc_info["Wind"]==1:
                airc_info["Wind"]="低"
            if airc_info["Wind"] == 2:
                airc_info["Wind"] = "中"
            if airc_info["Wind"] == 3:
                airc_info["Wind"] = "高"
    return render(request,'AirCManager.html',{'list':airc_info_list,'result1':result1,'result2':result2,'config':config_info})


def TurnOn(request):
    session_check=request.session.get("username")
    if not session_check:
        return HttpResponseRedirect("../../")

    config_info.DefaultTemp=float(request.POST["default_temp"])
    config_info.Price=float(request.POST["default_price"])
    config_info.ProducerNum=int(request.POST["producer_num"])
    if request.POST["modle"]=="Cold":
        config_info.DefaultModle="Cold"
    else:
        config_info.DefaultModle="Hot"
    airclist = []
    for airc in models.AirC.objects.all():
        airclist.append(airc.room_num)
    controller.start(config_info,airclist)
    return HttpResponseRedirect("/AirCManager/")

#@login_required
def turnOff(request):
    session_check=request.session.get("username")
    if not session_check:
        return HttpResponseRedirect("../../")
    global prema
    getlist=models.UserRoom.objects.all()
    for var in getlist:
        controller.turnOffAirC(var.user_name,var.room)
    return HttpResponseRedirect("/AirCManager/")

#@login_required
def delAirC(request):
    session_check=request.session.get("username")
    if not session_check:
        return HttpResponseRedirect("../../")
    global prema
    id=request.POST.get('room')
    if id=='':
        return HttpResponse('空调号输入错误')
    result='success'
    search1=models.AirC.objects.filter(room_num=id)
    if search1.count()==0:
        prema.p2=0
        return HttpResponse('空调号输入错误')
    else:
        search2=models.UserRoom.objects.filter(room=id)
        if search2.count()>0:
            prema.p2=0
            return HttpResponse('空调号输入错误')
        else:
            controller.delAirC(roomNum=id)
    return HttpResponseRedirect("/AirCManager/")

#@login_required
def addAirC(request):
    session_check=request.session.get("username")
    if not session_check:
        return HttpResponseRedirect("../../")
    global prema
    id = request.POST.get('room')
    if id=='':
        return HttpResponse('空调号输入错误')
    prema.p1 = 'success'
    search1 = models.AirC.objects.filter(room_num=id)
    if search1.count()>0:
        prema.p1=0
    else:
        controller.addAirC(roomNum=id)
    return HttpResponseRedirect("/AirCManager/")


def logout(request):
    session_check=request.session.get("username")
    if not session_check:
        return HttpResponseRedirect("../../")
    del request.session["username"]  # 删除session
    return HttpResponseRedirect("../")