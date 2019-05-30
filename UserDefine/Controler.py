from UserDefine.ConfigReader import config_info
from 温控系统.models import AirC
import queue

#任务类
class Task:
    def __init__(self):
        pass

class AirCState:
    #空调状态类
    def __init__(self):
        self.roomNum=''
        self.wind=0;
        self.temp=0;
        self.user=None;

class Controller(object):
    #生成单例
    __instance=None
    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            cls.__instance=object.__new__(cls)
        return cls.__instance

    def __init__(self):
        #初始化状态信息
        self.config_info=config_info
        #初始化任务队列
        self.taskList=[]
        #初始化空调信息队列
        self.stateList=[]
        airCs=AirC.objects.all()

    #信息查询类函数->允许立即返回
    def getState(self):
        pass

    def getAllState(self):
        pass


    #控制类函数->立即返回，延迟操作
    def setAirCState(self):
        pass
