# Distributed-Temperature-Control-System
分布式温控系统

# 配置说明该
需要修改Distributed_Temperature_Control_System目录下的setting文件，具体步骤如下：
1. 在电脑上的mysql运行sql脚本创建数据库
2. DATABASES变量中修改USER,PASSWORD,PORT(我配置的使用用的mysql8.0因此可能端口号不一样)
3. 安装mysqlclient(可能会安装失败，所以提供了一个供3.7版本的在文件里,使用pip安装就行了)
4. 数据库的迁移，migrate
5. MySQL中如果使用的是8.0版本，启动项目会报错，一个关于数据库连接的错误，这里给出解决方法
    root登陆mysql
       use mysql
        alter user 'django_user'@'localhost' identified with mysql_native_password by '123456';
        (msyql8.0使用了SHA2验证，而django不支持)
        
# 关于git的使用
1. 保存，使用commit就可以保存到本地仓库了
2. 发布，在工具栏VCS下git，push就可以推送到远程的仓库了
3. 同步最新的仓库，pull就行了

# 风速
风速分为三档 分别用 1，2，3 表示 低、中、高三档

#接口
浏览器与模块：
	../login:get ：返回登陆页面
				post：../Customer
						../Front
						../HotelManager
						../AirCManager
						返回响应操作页面，session写入基本信息
	../logout:get：清空session
	../setPassWord:get:返回修改密码页面
						post：提交修改请求
//身份验证通过session检测，后面的页面在处理请求前检测就行了
	../Customer/turnOn:设置
				  /setTemp:
				  /setWind:
				  /getAccount:
				  /turnOff:
	../Front/login:用户注册
			  /getAccount;查询计费		
			  /logout：用户注销		  
	../AirCManager/turnOn:post启动中央空调
					  /turnOff:post关闭中央空调
					  /setState:post包含完整期望空调的状态
					  /setCharge:post设置计费系数
/checkState:get:返回页面
				  post:发出状态查看请求(用于页面刷新)
	              /addAirC:get：返回调整页
								  post：提交请求内容
                 /delAirC:get：返回目标页
								  post:提交请求内容
../HotelManager/startServic:post启动空调系统
					/setCharge:post设置计费系数
					/stopService:post停止服务
				   /getReport；get生成报表
					//修改用户信息这个有点怪，按需要填吧

控制器（直接调用Controller.py下的controller即可）：
def getStates(self)://获取所用空调的状态信息
//返回值是一个数组，每一个元素包含了roomNum,wind,temp,user
def getAccount(self,roomNum:str,userId:str):
//获取当前未结束的计费段的金额
def setDefaultConfig(self,temp:int ,wind: int ,charge: float):
//修改默认设置,返回值类型为bool
def startService(self)://启动服务
//返回值类型为bool
def stopService(self)://停止服务
//返回值类型为bool
def setAirCState(self,temp:int,wind:int)://设置空调状态
//返回值类型为bool
def turnOnAirC(self,userId:str,roomNum:str)://启动空调
//返回值类型为bool
def turnOffAirC(self,userId:str,roomNum:str)://关闭空调
//返回值类型为bool
默认参数的导入使用UserDefine目录下的ConfigReader.py中的config_info，具体内容自行查看
  