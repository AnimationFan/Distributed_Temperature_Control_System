import xml.sax
from os import path

class DefaultConfig:
    def __init__(self):
        #制热模式
        self.HotMaxTemp=0;
        self.HotMinTemp=0;
        #制冷模式
        self.ColdMaxTemp=0;
        self.ColdMinTemp=0;
        #默认温度
        self.DefaultTemp=0;
        self.DefaultModle='Cold';

        self.Price=0;

        #每度电可以使用的时间
        self.TimeInHigh=0;
        self.TimeInMiddle = 0;
        self.TimeInLow = 0;

        #不同风速下的速度变化时间
        self.TempChangeInHigh = 0;
        self.TempChangeInMiddle = 0;
        self.TempChangeInLow = 0;


class ConfigReader(xml.sax.ContentHandler):
    def __init__(self, defaultconfig:DefaultConfig):
        self.configInfo=defaultconfig

    #元素开始事件处理
    def startElement(self,tag,attributes):
        #数据操作
        if tag=="ini":
            #print("读取开始")
            pass
        if tag=="TempRange":
            if attributes['modle']=='Hot':
                #print("制热模式")
                #print("最高温度",attributes['max'])
                self.configInfo.HotMaxTemp=attributes['max']
                #print("最低温度",attributes['min'])
                self.configInfo.HotMinTemp = attributes['min']
            if attributes['modle']=='Cold':
                #print("制冷模式")
                #print("最高温度",attributes['max'])
                self.configInfo.ColdMaxTemp = attributes['max']
                #print("最低温度",attributes['min'])
                self.configInfo.ColdMinTemp = attributes['min']
        if tag=="DefaultTemp":
            self.configInfo.DefaultTemp=attributes['value']
            self.configInfo.DefaultModle=attributes['modle']
        if tag=="Price":
            #print("默认价格",attributes['value'])
            self.configInfo.Price=attributes['value']
        if tag=="UseTime":
            if attributes['modle']=='HighWind':
                #print("高风速使用时间",attributes['time'])
                self.configInfo.TimeInHigh=attributes['time']
            if attributes['modle'] == 'MiddleWind':
                #print("中风速使用时间", attributes['time'])
                self.configInfo.TimeInMiddle = attributes['time']
            if attributes['modle'] == 'LowWind':
                #print("低风速使用时间", attributes['time'])
                self.configInfo.TimeInLow = attributes['time']
        if tag=="ChangeSpeed":
            if attributes['modle'] == 'HighWind':
                #print("高风速变化速度", attributes['speed'])
                self.configInfo.TempChangeInHigh=attributes['speed']
            if attributes['modle'] == 'MiddleWind':
                #print("中风速变化速度", attributes['speed'])
                self.configInfo.TempChangeInMiddle=attributes['speed']
            if attributes['modle'] == 'LowWind':
                #print("低风速变化速度", attributes['speed'])
                self.configInfo.TempChangeInLow=attributes['speed']

    #元素结束事件处理
    def endElement(self,tag):
        pass

    #内容事件处理
    def charsets(self,content):
        pass


# 读取配置信息到目标对象
config_info = DefaultConfig()
#创建一个XMLReader
parser=xml.sax.make_parser();

# turn off namepsaces
parser.setFeature(xml.sax.handler.feature_namespaces, 0)

# 重写 ContextHandler
Handler = ConfigReader(config_info)
parser.setContentHandler(Handler)
parser.parse("static/Configure.xml")

#print(configInfo)