from django.shortcuts import render_to_response


from UserDefine.Controller import Controller,controller
from 温控系统 import models
from UserDefine.ConfigReader import config_info,DefaultConfig

# -*- coding: UTF-8 -*-

Default=DefaultConfig()

controller=Controller()

class Customer:
    id=''
    room=''

    def welcome(self,request):
      self.id = request.GET['id']
      self.room = request.GET['room']
      pre = models.UserRoom.Object.get(User_name=self.id)
      preroom=pre.room.room_num
      return render_to_response('welcome.html',{'room':preroom})

    #开启空调
    def turnOn(self,request):
      global controller
      controller.turnOnAirC(self.id,self.room)
      return render_to_response('Customer.html')

    #设置温度
    def settemp(self,request):
      global controller
      lastone = controller.getStates();
      t = request.GET['temp']
      t = int(t)
      w=lastone['Temp']
      controller.setAirCState(t,w)
      return render_to_response('Customer.html')

    #设置风速
    def settemp(self,request):
      global controller
      lastone = controller.getStates();
      w = request.GET['wind']
      w = int(w)
      t=lastone['Temp']
      controller.setAirCState(t,w)
      return render_to_response('Customer.html')


    def getAccount(self,request):
      global controller
      list=models.UseRecord.objects.filter(room_num=precus.room)
      totalcost=0.0
      for var in list:
        totalcost=totalcost+var.price
      return render_to_response('Customer.html',{'cost':totalcost})


    def turnOff(self,request):
      global controller
      controller.turnOnAirC(self.id,self.room)
      return render_to_response('Customer.html')

precus=Customer()



