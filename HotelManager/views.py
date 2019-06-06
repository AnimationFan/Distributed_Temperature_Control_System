from django.shortcuts import render_to_response
from django.shortcuts import render

from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from UserDefine.Controller import Controller,controller
from 温控系统 import models
from UserDefine.ConfigReader import config_info,DefaultConfig

# -*- coding: UTF-8 -*-

Default=DefaultConfig()

class Manager:

    pretemp=Default.DefaultTemp
    precharge=Default.Price
    def __init__(self):
        pass

prema=Manager()

#@login_required
def welcome(request):
    global controller,prema
    getlist = controller.getStates()
    showlist=[]
    for var in getlist:
      seacus=models.UserRoom.objects.all()
      for var2 in seacus:
          if var2.room.room_num==var['RoomNum']:
              precus=var2.user_name.user_name
              a = {"customer": precus, "room": var['RoomNum']}
              showlist.append(a)
    return render(request,'HotelManager.html',{"list":showlist,'temp':prema.pretemp,'charge':prema.precharge})


    #设置计费参数
#@login_required
def setCharge(request):
    global controller,prema
    newcharge = request.POST.get('charge')
    newtemp = config_info.DefaultTemp
    newcharge = float(newcharge)
    controller.setDefaultConfig(newtemp, newcharge)
    prema.precharge=newcharge
    return HttpResponseRedirect("/HotelManager/")


#@login_required
def setTemp(request):
    global controller,prema
    newtemp = request.POST.get('temp')
    newcharge = config_info.Price
    newtemp = float(newtemp)
    controller.setDefaultConfig(newtemp, newcharge)
    prema.pretemp=newtemp
    return HttpResponseRedirect("/HotelManager/")


    #开启空调
#@login_required
def getReport(request):
    global controller,prema
    customer = request.POST.get('customerID')
    room = request.POST.get('roomID')

    runningtimes=0
    targettem = 0
    targetwind = 0

    alltem = []
    allwind = []

    #到达温度次数
    seacus=models.User.objects.filter(user_name=customer)
    if seacus.count()==0:
        return HttpResponse(customer)
    precus=seacus.get(user_name=customer)
    searoom = models.AirC.objects.filter(room_num=room)
    if searoom.count() == 0:
        return HttpResponse("查找失败2")
    preroom = searoom.get(room_num=room)
    seauserroom=models.UserRoom.objects.filter(user_name=precus,room=preroom)

    getlist = models.UseRecord.objects.filter(user_name=customer,room_num=room)
    length=len(getlist)

    if seauserroom.count()==0:
        return HttpResponse("查找失败3")
    pre = seauserroom.get(user_name=precus)

    #到达目标温度次数
    reachtemtimes = pre.reachtimes

    for i in range(0,length-1):

         # 记录运行次数
      if (getlist[i].end_time!=getlist[i+1].begin_time):
           runningtimes+1


      #记录全部风速、温度
      alltem.append(getlist[i].temp)
      allwind.append(getlist[i].wind)

       # 记录最大的次数的温度
    d = {}
    for i in alltem:
      if i not in d:
        count = alltem.count(i)
        d[i] = count
      if count > d.get(targettem, 0):
        targettem = i

       # 记录最大的次数的风速
    e = {}
    for i in allwind:
      if i not in e:
        count = allwind.count(i)
        e[i] = count
      if count > d.get(targetwind, 0):
        targetwind = i

       #记录调度次数
    preid=models.UserRoom.objects.get(user_name=precus,room=preroom)
    preid.schedulingtimes=preid.schedulingtimes+1
    schedulingtimes=preid.schedulingtimes

       #总记录数
    notesnum=len(getlist)

       #总开销
    totalcost = 0.0
    for var in getlist:
      totalcost = totalcost + var.price
    totalcost = totalcost + controller.getAccount(customer, room)

    return render_to_response('Report.html',{'runningtimes': runningtimes,"targettem":targettem,'targetwind':targetwind,"schedulingtimes":schedulingtimes,"reachtemtimes":reachtemtimes,"notesnum":notesnum,"totalcost":totalcost})

