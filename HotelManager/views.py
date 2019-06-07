from django.shortcuts import render_to_response
from django.shortcuts import render

from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from UserDefine.Controller import Controller,controller
from 温控系统 import models
from UserDefine.ConfigReader import config_info,DefaultConfig

# -*- coding: UTF-8 -*-


class Manager:

    pretemp=config_info.DefaultTemp
    precharge=config_info.Price
    def __init__(self):
        pass

prema=Manager()

#@login_required
def welcome(request):
    session_check=request.session.get("username")
    if not session_check:
        return HttpResponseRedirect("../")
    if session_check!='1001':
        return HttpResponseRedirect("../")
    global controller,prema
    getlist = controller.getStates()
    showlist=[]
    for var in getlist:
      seacus=models.UserRoom.objects.all()
      for var2 in seacus:
          if var2.room==var['RoomNum']:
              precus=var2.user_name
              a = {"customer": precus, "room": var['RoomNum']}
              showlist.append(a)
    prema.pretemp=config_info.DefaultTemp
    prema.precharge=config_info.Price
    return render(request,'HotelManager.html',{"list":showlist,'temp':prema.pretemp,'charge':prema.precharge})


    #设置计费参数
#@login_required
def setCharge(request):
    session_check=request.session.get("username")
    if not session_check:
        return HttpResponseRedirect("../../")
    if session_check!='1001':
        return HttpResponseRedirect("../../")
    global controller,prema
    newcharge = request.POST.get('charge')
    newtemp = config_info.DefaultTemp
    newcharge = float(newcharge)
    controller.setDefaultConfig(newtemp, newcharge)
    prema.precharge=newcharge
    return HttpResponseRedirect("/HotelManager/")


#@login_required
def setTemp(request):
    session_check=request.session.get("username")
    if not session_check:
        return HttpResponseRedirect("../../")
    if session_check!='1001':
        return HttpResponseRedirect("../../")
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
    session_check=request.session.get("username")
    if not session_check:
        return HttpResponseRedirect("../../")
    if session_check!='1001':
        return HttpResponseRedirect("../../")
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
        return HttpResponse("查找不能为空")
    precus=seacus.get(user_name=customer)
    searoom = models.AirC.objects.filter(room_num=room)
    if searoom.count() == 0:
        return HttpResponse("房间不存在")
    preroom = searoom.get(room_num=room)
    seauserroom=models.UserRoom.objects.filter(user_name=customer,room=room)

    getlist = models.UseRecord.objects.filter(user_name=customer,room_num=room)
    length=len(getlist)

    if seauserroom.count()==0:
        return HttpResponse("无居住记录")
    pre = seauserroom.get(user_name=customer)

    #到达目标温度次数
    reachtemtimes = pre.reachtimes

    for i in range(0,length-1):

         # 记录运行次数
      if (getlist[i].end_time!=getlist[i+1].begin_time):
           runningtimes+1


      #记录全部风速、温度
      alltem.append(getlist[i].temp)
      allwind.append(getlist[i].wind)


       # 记录最大的时间的温度
    d = {}
    current_maxtime=0             #初始化计算最长时间
    for i in alltem:
      if i not in d:
        count=0
        for var in getlist:
          if var.temp==i:
              count = count+(var.end_time-var.begin_time).seconds          #计算当前目标温度经过时间
        d[i] = count
      if count > current_maxtime:
        targettem = i
        current_maxtime=count

       # 记录最大的时间的风速
    e = {}
    current_maxtime = 0  # 初始化计算最长时间
    for i in allwind:
        if i not in d:
            count = 0
            for var in getlist:
                if var.wind == i:
                    count = count + (var.end_time - var.begin_time).seconds  # 计算当前目标温度经过时间
            d[i] = count
        if count > current_maxtime:
            targetwind = i
            current_maxtime = count

       #记录调度次数
    preid=models.UserRoom.objects.get(user_name=customer,room=room)
    preid.schedulingtimes=preid.schedulingtimes+1
    schedulingtimes=preid.schedulingtimes

       #总记录数
    notesnum=len(getlist)

       #总开销
    totalcost = 0.0
    for var in getlist:
      totalcost = totalcost + var.price
    totalcost = totalcost + controller.getAccount(customer, room)
    if controller.getAccount(customer, room)==-1:
        totalcost=totalcost+1
    totalcost = round(totalcost,1)

    return render_to_response('Report.html',{'runningtimes': runningtimes,"targettem":targettem,'targetwind':targetwind,"schedulingtimes":schedulingtimes,"reachtemtimes":reachtemtimes,"notesnum":notesnum,"totalcost":totalcost})

def logout(request):
    session_check=request.session.get("username")
    if not session_check:
        return HttpResponseRedirect("../../")
    if session_check!='1001':
        return HttpResponseRedirect("../../")
    del request.session["username"]  # 删除session
    return HttpResponseRedirect('../../')