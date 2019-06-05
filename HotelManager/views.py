from django.shortcuts import render_to_response

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from UserDefine.Controller import Controller,controller
from 温控系统 import models
from UserDefine.ConfigReader import config_info,DefaultConfig

# -*- coding: UTF-8 -*-

Default=DefaultConfig()

class Manager:

    def __init__(self):
        pass

preMa=Manager()

#@login_required
def welcome(request):
    getlist = []
    getlist = controller.getStates()
    for var in getlist:
      a = {"customer": var['user_name'], "room": var['room']}
      getlist.append(a)
    return render_to_response('Mawelcome.html',{"list":getlist})


    #设置计费参数
@login_required
def setCharge(request):
    global controller,prema
    newcharge = request.GET['charge']
    newtemp = config_info.DefaultTemp
    controller.setDefaultConfig(newtemp, newcharge)
    HttpResponseRedirect("/Manager/")

@login_required
def setTemp(request):
    global controller,prema
    newtemp = request.GET['temp']
    newcharge = config_info.Price
    controller.setDefaultConfig(newtemp, newcharge)
    HttpResponseRedirect("/Manager/")


    #开启空调
@login_required
def getReport(request):
    global controller,prema
    customer = request.GET['customerID']
    room = request.GET['roomID']

    getlist = models.UseRecord.objects.filter(room_num=room,user_name=customer)
    length=len(getlist)

    runningtimes=0
    targettem = 0
    targetwind = 0
    reachtemtimes=0

    alltem = []
    allwind = []

    defaulttem=config_info.DefaultTemp
    currenttem=defaulttem

    #到达温度次数
    pre = models.UserRoom.objects.get(user_name=customer)
    reachtemtimes = pre.reachtimes

    for i in range(0,length-1):

         # 记录运行次数
      if (getlist[i].end_time!=getlist[i+1].begin_time):
           runningtimes+1
           temdepart = abs(defaulttem - currenttem)
           reachtime = temdepart * 5
           timedepart = (getlist[i+1].begin_time - getlist[i].end_time).total_seconds()/60
           if (timedepart > reachtime):
             currenttem = defaulttem
           else:
               if defaulttem > currenttem:
                   currenttem = currenttem + timedepart / 5
               else:
                   currenttem = currenttem - timedepart / 5

         #记录到达目标温度次数
     #temdepart = abs(getlist[i].temp-currenttem)
         #reachtime = temdepart*5
         #timedepart = (getlist[i].begin_time - getlist[i].end_time).total_seconds()/60
         #if (timedepart>reachtime):
             #reachtemtimes=reachtemtimes+1
             #currenttem=getlist[i].temp
         #else:
             #if getlist[i].temp>currenttem:
                #currenttem=currenttem+timedepart/5
             #else:
                 #currenttem=currenttem-timedepart/5


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
    preid=models.UserRoom.objects.get(user_name=customer)
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

