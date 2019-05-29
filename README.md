# Distributed-Temperature-Control-System
分布式温控系统

# 配置说明该
需要修改Distributed_Temperature_Control_System目录下的setting文件，具体步骤如下：
1. 在电脑上的mysql运行sql脚本创建数据库
2. DATABASES变量中修改USER,PASSWORD,PORT(我配置的使用用的mysql8.0因此可能端口号不一样)
3. 安装mysqlclient(可能会安装失败，所以提供了一个供3.7版本的在文件里,使用pip安装就行了)
4. 数据库的迁移，migrate

# 关于git的使用
1. 保存，使用commit就可以保存到本地仓库了
2. 发布，在工具栏VCS下git，push就可以推送到远程的仓库了
3. 同步最新的仓库，pull就行了