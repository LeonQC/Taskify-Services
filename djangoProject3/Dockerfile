# Dockerfile

# 使用官方的Python基础镜像
FROM python:3.8-slim

# 设置工作目录
WORKDIR /code

# 将requirements.txt复制到容器中
COPY requirements.txt /code/

# 安装Python依赖
RUN pip install --no-cache-dir -r requirements.txt

# 将当前目录复制到容器中
COPY . /code/

# 暴露Django默认端口
EXPOSE 8000

# 启动命令
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
