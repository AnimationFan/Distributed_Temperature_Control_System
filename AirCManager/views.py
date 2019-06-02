from django.shortcuts import render_to_response

from UserDefine.Controller import Controller,controller
from 温控系统 import models
from UserDefine.ConfigReader import config_info,DefaultConfig

# -*- coding: UTF-8 -*-

class AirCManager:

    def welcome(self,request):
      global controller
      list=[]
      getlist = controller.getStates()
      for var in getlist:
        a={"customer":var.user_name,"room":var.room,"on":"关"}
        if var["On"]==True:
            a["on"]="开"
        list.append(a)
      return render_to_response('welcome.html',{'list':list})

    #开启中央空调
    def turnOn(self,request):
      global controller
      list=models.UserRoom.objects.all()
      for var in list:
          controller.turnOnAirC(var.user_name,var.room)
      return render_to_response('AirCManager.html')

    def turnOff(self,request):
      global controller
      list=models.UserRoom.objects.all()
      for var in list:
          controller.turnOffAirC(var.user_name,var.room)
      return render_to_response('AirCManager.html')
    
    def delAirC(self,request):
      global controller
      id=request.GET['room']
      result='success'
      search1=models.AirC.objects.filter(user=id)
      if search1.count()==0:
          result='error'
      else:
          search2=models.UserRoom.objects.filter(user_name=id)
          if search2.count()>0:
              result='error'
          else:
              models.AirC.objects.filter(user='id').delete()
      return render_to_response('AirCManager.html',{"result":result})
    
    def addAirC(self,request):
      global controller
      id = request.GET['room']
      result = 'success'
      search1 = models.AirC.objects.filter(user=id)
      if search1.count()>0:
          result='error'
      else:
          models.AirC.objects.create(room_num=id)
      return render_to_response('AirCManager.html',{"result":result})

prema=AirCManager()

