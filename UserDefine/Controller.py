from UserDefine.ConfigReader import config_info,DefaultConfig
from 温控系统.models import AirC,UseRecord

import datetime
import threading
import time

#任务类
class Task:
    def __init__(self,roomNum:str,temp:int,wind,userId:str):
        self.targetRoom=roomNum
        self.targetTemp=temp
        self.targetWind=wind
        self.userId=userId

#任务队列，
class TaskList:
    def __init__(self):
        self.List=[]
        pass


#状态记录类，实际已经相当于空调的实例了
class AirCState(threading.Thread):
    #空调状态类
    def __init__(self,roomNum:str,config:DefaultConfig):
        self.on=False
        self.roomNum=roomNum
        self.wind=0
        self.user=''
        self.begintime=None
        self.defaultconfig=config
        self.temp = self.defaultconfig.DefaultTemp
        self.targetTemp=self.defaultconfig.DefaultTemp
        self.semaphore=threading.Semaphore(1)#对空调状态修改的semahore

    def getPrice(self):
        endtime = datetime.datetime.now()
        usetime = (endtime.day - self.begintime.day) * 24 * 60 + (endtime.hour - self.begintime.hour) * 60 + (
                    endtime.minute - self.begintime.minute)
        price = 0
        if self.wind == 1:  # 低档风
            price = (usetime / self.defaultconfig.TimeInLow) * self.defaultconfig.Price
        if self.wind == 2:  # 中档风
            price = (usetime / self.defaultconfig.TimeInMiddle) * self.defaultconfig.Price
        if self.wind == 3:  # 高档风
            price = (usetime / self.defaultconfig.TimeInHigh) * self.defaultconfig.Price
        return price

    def saveRecord(self):
        #保存
        endtime=datetime.datetime.now()
        record=UseRecord(begin_time=self.begintime,
                         end_time=endtime,
                         user_name=self.user,
                         room_num=self.roomNum,
                         wind=self.wind,
                         temp=self.targetTemp,
                         price=self.getPrice()
                         )
        self.begintime=datetime.datetime.now()

    def run(self):
        while True:
            if self.On==False:
                #若空调处于关闭状态，则按照每分钟0.5度的方式变化
                if self.temp!=self.defaultconfig.DefaultTemp:
                    self.semaphore.acquire()
                    if self.temp>self.defaultconfig.DefaultTemp and self.temp-0.5>self.defaultconfig.DefaultTemp:
                        self.temp=self.temp-0.5
                    else:
                        self.temp=self.defaultconfig.DefaultTemp
                    if self.temp<self.defaultconfig.DefaultTemp and self.temp+0.5<self.defaultconfig.DefaultTemp:
                        self.temp=self.temp+0.5
                    else:
                        self.temp=self.defaultconfig.DefaultTemp
                    self.semaphore.release()
            if self.On==True:
                if self.temp!=self.targetTemp:
                    if self.wind==1:#低档风
                        pass
                    if self.wind==2:#中档风
                        pass
                    if self.wind==3:#高档风
                        pass
            time.sleep(60)




#任务处理类，负责处理任务
class Producer(threading.Thread):
    def __init__(self,RWSemaphore:threading.Semaphore,
                 TaskSemaphore:threading.Semaphore,
                 aircList:list,TaskList:list,task:Task):
        threading.Thread.__init__(self)#指定了部分变量的类型，主要是为了方便后续的编码，记得Task初始必须为None
        self.rwSemaphore=RWSemaphore
        self.taskSemaphore=TaskSemaphore
        self.taskList=TaskList
        self.currentTask=task   #当前执行任务
        self.aircList=aircList

    def  run(self):
        while self.taskSemaphore.acquire():
            if self.rwSemaphore.acquire():
                #结束当前执行的任务
                if self.currentTask:
                    #查找当前的空调对象，保存记录
                    pass
                #读取第一个任务

#控制类，提供同一的任务管理方法，处理任务的调度
class Controller(object):
    #生成单例
    __instance=None
    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            cls.__instance=object.__new__(cls)
        return cls.__instance

    def __init__(self):
        self.config_info=config_info#初始化状态信息
        self.taskList = []# 初始化任务队列
        self.producers=[]#初始化处理器队列
        i=0
        while i<self.config_info.ProducerNum:
            self.producers.append(Producer())
            i=i+1
        self.aircList=[]#初始化空调信息队列
        airCs=AirC.objects.all()
        for airc in airCs:
           self.aircList.append(AirCState(airc.room_num))

    #信息查询类函数->允许立即返回
    def getStates(self):
        result=[]
        for airc in self.aircList:
            aircstate={"RoomNum":airc.roomNum,"Temp":airc.temp,"Wind":airc.wind,"User":airc.user,"Price":airc.getPrice()}
            result.append(aircstate)
        return airc

    def getAccount(self,roomNum:str,userId:str):
        price=-1;#返回-1表示出错，可能位roomNum或者userId错误
        for airc in self.aircList:
            if airc.roomNum==roomNum and airc.user==userId:
                price=airc.getPrice()
        return price



    #控制类函数->立即返回，延迟操作
    def setDefaultConfig(self,temp:int ,wind: int ,charge: float):
        pass

    def startService(self):
        pass

    def stopService(self):
        pass

    def setAirCState(self,temp:int,wind:int):
        pass

    def turnOnAirC(self,userId:str,roomNum:str):
        pass

    def turnOffAirC(self, userId: str, roomNum: str):
        pass

controller=Controller()