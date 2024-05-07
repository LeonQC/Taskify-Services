
# 如何在docker上安装MongoDB

## **前置：**
1.安装 Docker desktop

2.安装mongosh或在之后在Docker用代码安装（不用人工定位软件位置）


## **步骤**

### **1.拉取 MongoDB Docker 映像**

docker pull mongodb/mongodb-community-server:latest

查看本地镜像
使用以下命令来查看是否已安装了 mongo：

$ docker images

![docker mongo4](file:///C:/Users/大BOSS晖爷/Desktop/docker-mongo4.png)


### **2.将映像作为 container 运行**

docker run -d -p 27017:27017 --name my-mongo-container mongo
参数说明：

-d: 后台运行容器。
-p 27017:27017: 将主机的27017端口映射到容器的27017端口。
--name my-mongo-container: 为容器指定一个名字，这里是my-mongo-container，你可以根据需要更改。

例如，要运行 MongoDB 5.0，请执行以下操作：

docker run --name mongodb -p 27017:27017 -d mongodb/mongodb-community-server:5.0-ubuntu2004


### 3.检查 container 正在运行

要检查 Docker container 的状态，请运行以下命令：

docker container ls

ls 命令的输出列出了描述正在运行的 container ，例如：


Container ID

Image

Command

Created

Status

Port

Names


### 4.使用 mongosh

mongosh --port 27017

### 5.验证
要确认 MongoDB 实例正在运行，请运行 Hello 命令：

db.runCommand(
   {
      hello: 1
   }
)

此命令的结果返回一个描述 mongod 部署的文档：

![微信图片 20240507230817](file:///C:/Users/大BOSS晖爷/Desktop/微信图片_20240507230817.png)

此时应该能够看到名为 my-mongo-container 的 MongoDB 容器正在运行。


### 6.连接MongoDB 客户端

接下来我们可以使用 MongoDB 客户端（例如 mongo shell）连接到运行中的 MongoDB 容器。

可以使用以下命令连接到 MongoDB：

$ mongosh --host 127.0.0.1 --port 27017

这将连接到本地主机的 27017 端口，你可以根据之前映射的端口进行调整。

进入 MongoDB 容器的 bash shell 命令如下：

docker exec -it my-mongo-container bash

在不再需要时停止和删除容器，可以使用以下命令：
docker stop my-mongo-container
docker rm my-mongo-container