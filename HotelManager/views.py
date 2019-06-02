from django.shortcuts import render_to_response


from UserDefine.Controller import Controller,controller
from 温控系统 import models
from UserDefine.ConfigReader import config_info,DefaultConfig

# -*- coding: UTF-8 -*-

Default=DefaultConfig()

controller=Controller()

class Manager:

    def welcome(self,request):
      return render_to_response('Mawelcome.html')

    #设置计费参数
    def setCharge(self,request):
        global controller
        newcharge = request.GET['charge']
        newwind = 调用函数
        controller.setDefaultConfig(newtemp, newcharge)
        return render_to_response('Manager.html')

    def setTemp(self,request):
        global controller
        newtemp = request.GET['temp']
        newcharge = 调用函数
        controller.setDefaultConfig(newtemp, newcharge)
        return render_to_response('Manager.html')

    #开启空调
    def getReport(self,request):
       global controller
       customer = request.GET['customerID']
       room = request.GET['roomID']

       list = models.UseRecord.objects.filter(room_num=room,user_name=customer)
       length=len(list)

       runningtimes=0
       targettem = 0
       targetwind = 0
       reachtemtimes=0

       alltem = []
       allwind = []

       defaulttem=调用函数
       currenttem=defaulttem
       
       for i in range(0,length-1):

         # 记录运行次数
         if (list[i].end_time!=list[i+1].begin_time):
             runningtimes+1
             temdepart = abs(defaulttem - currenttem)
             reachtime = temdepart * 5
             timedepart = (list[i+1].begin_time - list[i].end_time).total_seconds()/60
             if (timedepart > reachtime):
                 currenttem = defaulttem
             else:
                 if defaulttem > currenttem:
                     currenttem = currenttem + timedepart / 5
                 else:
                     currenttem = currenttem - timedepart / 5

         #记录到达目标温度次数
         temdepart = abs(list[i].temp-currenttem)
         reachtime = temdepart*5
         timedepart = (list[i].begin_time - list[i].end_time).total_seconds()/60
         if (timedepart>reachtime):
             reachtemtimes=reachtemtimes+1
             currenttem=list[i].temp
         else:
             if list[i].temp>currenttem:
                 currenttem=currenttem+timedepart/5
             else:
                 currenttem=currenttem-timedepart/5

         #记录全部风速、温度
         alltem.append(list[i].temp)
         allwind.append(list[i].wind)

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
       notessum=len(list)

       #总开销
       totalcost = 0.0
       for var in list:
           totalcost = totalcost + var.price
       totalcost = totalcost + controller.getAccount(customer, room)

       return render_to_response('Manager.html',{'runningtimes': runningtimes,"targettem":targettem,'targetwind':targetwind,"schedulingtimes":schedulingtimes,"reachtemtimes":reachtemtimes,"notesnum":notesnum,"totalcost":totalcost})

preMa=Manager()
