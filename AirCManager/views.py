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

    @login_required
    def welcome(self,request):
      global controller
      if self.p1==1:
          result1='success'
      else:
          result1='error'
          self.p1=0
      if self.p2==1:
          result2='success'
      else:
          result2='error'
          self.p2=0
      list=[]
      getlist = controller.getStates()
      for var in getlist:
        a={"customer":var.user_name,"room":var.room,"on":"关"}
        if var["On"]==True:
            a["on"]="开"
        list.append(a)
      return render_to_response('welcome.html',{'list':list,'result1':result1,'result2':result2})

    #开启中央空调
    @login_required
    def turnOn(self,request):
      global controller
      list=models.UserRoom.objects.all()
      for var in list:
          controller.turnOnAirC(var.user_name,var.room)
      return HttpResponseRedirect("/AirCManager/")

    @login_required
    def turnOff(self,request):
      global controller
      list=models.UserRoom.objects.all()
      for var in list:
          controller.turnOffAirC(var.user_name,var.room)
      return HttpResponseRedirect("/AirCManager/")

    @login_required
    def delAirC(self,request):
      global controller
      id=request.GET['room']
      result='success'
      search1=models.AirC.objects.filter(user=id)
      if search1.count()==0:
          self.p2=0
      else:
          search2=models.UserRoom.objects.filter(user_name=id)
          if search2.count()>0:
              self.p2=0
          else:
              models.AirC.objects.filter(user='id').delete()
      return HttpResponseRedirect("/AirCManager/")

    @login_required
    def addAirC(self,request):
      global controller
      id = request.GET['room']
      result = 'success'
      search1 = models.AirC.objects.filter(user=id)
      if search1.count()>0:
          self.p1=0
      else:
          models.AirC.objects.create(room_num=id)
      return HttpResponseRedirect("/AirCManager/")

prema=AirCManager()

