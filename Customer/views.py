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
    targettem=1

    def __init__(self):
        self.targettem=Default.DefaultTemp

    @login_required
    def welcome(self,request):
      self.id = request.GET['id']
      pre = models.UserRoom.object.get(User_name=self.id)
      preroom=pre.room.room_num
      self.room=preroom
      temp=self.targettem
      return render_to_response('welcome.html',{'room':preroom,'temp':temp})

    #开启空调
    @login_required
    def turnOn(self,request):
      global controller
      controller.turnOnAirC(self.id,self.room)
      HttpResponseRedirect("/Customer/")

    #设置温度
    @login_required
    def setTemp(self,request):
      global controller
      last = controller.getStates();
      for var in last:
          if var["RoomNum"]==self.room:
              lastone=var
      t = request.GET['temp']
      t = int(t)
      w=lastone['Temp']
      controller.setAirCState(self.room,t,w,self.id)
      HttpResponseRedirect("/Customer/")

    #设置风速
    @login_required
    def setWind(self,request):
      global controller
      last = controller.getStates();
      for var in last:
          if var["RoomNum"] == self.room:
              lastone = var
      w = request.GET['wind']
      w = int(w)
      t=lastone["Temp"]
      controller.setAirCState(self.room,t,w,self.id)
      HttpResponseRedirect("/Customer/")


    @login_required
    def getAccount(self,request):
      global controller
      list=models.UseRecord.objects.filter(room_num=precus.room)
      totalcost=0.0
      for var in list:
        totalcost=totalcost+var.price
      totalcost=totalcost+controller.getAccount(self.id,self.room)
      return render_to_response('Customer.html',{'cost':totalcost})


    @login_required
    def turnOff(self,request):
      global controller
      controller.turnOnAirC(self.id,self.room)
      HttpResponseRedirect("/Customer/")


precus=Customer()



