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
        self.beginTime=None
        self.timer=None

    def timerWork(self,taskList):
        producer=taskList.getProducer()
        producer.releaseTask()
        producer.setTask(self)



#任务队列，实质是任务的控制分配系统系统
class TaskList:
    def __init__(self):
        self.taskList=[]
        self.task_semaphore=threading.Semaphore(1)
        self.producerList=[]
        self.producer_semaphore=threading.Semaphore(1)

    def appendProducer(self,producer):
        self.producer_semaphore.acquire()
        self.producerList.append(producer)
        self.producer_semaphore.release()

    def addTask(self,task:Task):
        vacant_producer=None
        self.producer_semaphore.acquire()
        for producer in self.producerList:
            if producer.task==None:
                vacant_producer=producer
                break
        if vacant_producer:
            vacant_producer.setTask(task)
            self.producer_semaphore.release()
        else:
            lowwer=[]
            equal=[]
            higher=[]
            for producer in self.producerList:
                if producer.task.targetWind < task.targetWind:
                    lowwer.append(producer)
                elif producer.task.targetWind == task.targetWind:
                    equal.append(producer)
                elif producer.task.targetWind == task.targetWind:
                    higher.append(producer)
            #有风速小于请求
            if lowwer.__len__()>0:
                if lowwer.__len__()==1:
                    lowwer[0].releaseTask()
                    lowwer[0].setTask(task)
                #出现了复数个时，那么选择一个风速最小，（全部相等时选择服务时间最长的）
                if lowwer.__len__()> 1:
                    best_producer=lowwer[0]
                    for producer in lowwer:
                        if producer.task.targetWind < best_producer.task.targetWind:
                            best_producer = producer
                            continue
                        elif producer.task.targetWind == best_producer.task.targetWind and producer.task.beginTime < best_producer.task.beginTime:
                           best_producer = producer
                    best_producer.releasTask()
                    best_producer.setTask(task)
            #没有风速小于，存在风速等于请求
            if lowwer.__len__()==0 and equal.__len__()>0:
                self.append(task)
                task.timer=threading.Timer(120,task.timerWork)
            #所有风速都大于请求
            if lowwer.__len__()==0 and equal.__len__()==0:
                self.appendTask(task)
            self.producer_semaphore.release()

    def getTask(self,wind):#选择队列当中存在计时器的
        best_task=None
        self.task_semaphore.acquire()
        for task in self.taskList:
            if best_task==None:
                best_task=task
                continue
            else:
                if task.timer!=None:
                    best_task=task
                    break
        self.task_semaphore.release()
        return best_task

    #AppendTask 主要用于风机释放之前的任务
    def appendTask(self,task:Task):
        self.task_semaphore.acquire()
        self.taskList.append(task)
        self.task_semaphore.release()

    #从当前队列当中强行释放一个producer
    def getProducer(self):
        best_producer=None
        for producer in self.producerList:
            if best_producer==None or (best_producer!=None and producer.task.beginTime<best_producer.task.beginTime):
                best_producer=producer
        return producer

#任务处理类，负责处理任务
class Producer():
    def __init__(self,taskList:TaskList,aircs:list):
        self.control_airc=None
        self.Task=None
        self.aircs=aircs
        self.taskList=taskList

    def setTask(self,task:Task):
        if task==None:
            return
        else:
            for airc in self.aircs:
                if airc.room_num==task.targetRoom and airc.user==task.userId:
                    self.task=task
                    self.task.beginTime=datetime.datetime.now()
                    self.control_airc=airc
                    self.control_airc.setProducer(self)
                    self.control_airc.setTask(task)

    def removeTask(self):#任务完成直接移除当前的任务
        self.control_airc=None
        wind=0
        if self.Task != None:
            wind=self.task.targetWind
            self.Task=None
        #从taskList获取任务
        task=self.taskList.getTask(wind)
        self.setTask(task)

    def releaseTask(self):#释放当前正在执行的任务
        self.control_airc=None
        if self.Task!=None:
            self.appendTask(self.task)
            self.task=None
            self.control_airc=None


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
        self.semaphore=threading.Semaphore(1)#对空调temp修改的semahore
        self.producer=None


    def turnOff(self,userId):
        #结束当前的任务，结束计费段
        self.saveRecord()
        self.begintime=None
        self.on=False
        self.wind=0
        self.user=''
        #出让服务对象
        self.producer.removeTask()
        return True

    def getPrice(self):
        price =0;
        if self.on == True:
            endtime = datetime.datetime.now()
            usetime = (endtime.day - self.begintime.day) * 24 * 60 + (endtime.hour - self.begintime.hour) * 60 + (
                    endtime.minute - self.begintime.minute)
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
        self.begintime=None


    def setTask(self,task:Task):
        self.semaphore.acquire()
        self.on=True
        self.wind=task.targetWind
        self.targetTemp=task.targetTemp
        self.user=task.userId
        self.begintime=datetime.datetime.now()
        self.semaphore.release()
        pass

    #run函数，根据设置，调整空调的温度，
    def run(self):
        while True:
            if self.on == False:
                # 若空调处于关闭状态，则按照每分钟0.5度的方式变化
                if self.temp != self.defaultconfig.DefaultTemp:
                    self.semaphore.acquire()
                    if self.temp > self.defaultconfig.DefaultTemp:
                        if self.temp - 0.5 > self.defaultconfig.DefaultTemp:
                            self.temp = self.temp - 0.5
                            continue
                        else:
                            self.temp = self.defaultconfig.DefaultTemp
                    elif self.temp < self.defaultconfig.DefaultTemp:
                        if self.temp + 0.5 < self.defaultconfig.DefaultTemp:
                            self.temp = self.temp + 0.5
                        else:
                            self.temp = self.defaultconfig.DefaultTemp
                    self.semaphore.release()
            if self.on == True and self.wind >= 1:
                TempChange = [self.defaultconfig.TempChangeInLow, self.defaultconfig.TimeInMiddle,
                              self.defaultconfig.TempChangeInHigh]
                self.semaphore.acquire()
                if self.defaultconfig.DefaultModle == "Cold":
                    self.temp = self.temp - TempChange[self.wind - 1]
                if self.defaultconfig.DefaultModle == "Hot":
                    self.temp = self.temp + TempChange[self.wind - 1]
                self.semaphore.release()
            time.sleep(60)

    def setProduer(self, producer:Producer):
        self.producer=producer


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
        self.aircList=[]#初始化空调信息队列,并启动
        airCs=AirC.objects.all()
        for airc in airCs:
            real_air=AirCState(airc.room_num)
            real_air.start()
            self.aircList.append(real_air)
        self.taskList = TaskList()
        i=0
        while i<self.config_info.ProducerNum:
            self.taskList.appendProducer(Producer(self.taskList,self.aircList))
            i=i+1


    #信息查询类函数->允许立即返回
    def getStates(self):
        result=[]
        for airc in self.aircList:
            aircstate={"RoomNum":airc.roomNum,"On":airc.on,"Temp":airc.temp,"Wind":airc.wind,"User":airc.user,"Price":airc.getPrice()}
            result.append(aircstate)
        return result

    def getAccount(self,roomNum:str,userId:str):
        price=-1;#返回-1表示出错，可能位roomNum或者userId错误
        for airc in self.aircList:
            if airc.roomNum==roomNum and airc.user==userId:
                price=airc.getPrice()
        return price



    #控制类函数->立即返回，延迟操作
    def setDefaultConfig(self,temp:int ,charge: float):
        # 所有启动的空调结束当前的计费段
        for airc in self.aircList:
            if airc.producer:
                airc.saveRecord()
                #刷新计费部分
                airc.begintime=datetime.datetime.now()
        self.config_info.DefaultTemp = temp
        self.config_info.Price = charge


    def setAirCState(self,roomNum:str,temp:int,wind:int,userId:str):
        self.taskList.addTask(Task(roomNum,temp,wind,userId))
        return True

    def turnOnAirC(self,userId:str,roomNum:str):
        self.taskList.addTask(Task(roomNum,self.config_info.DefaultTemp,1,userId))
        return True

    def turnOffAirC(self, userId: str, roomNum: str):
        for airc in self.aircList:
            if airc.roomNum ==roomNum and airc.user==userId:
                airc.turnOff()
                return True
        return False

controller=Controller()