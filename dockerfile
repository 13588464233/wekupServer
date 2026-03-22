FROM docker.io/library/python:3.10-slim

# 设置工作目录
WORKDIR /app

# 安装系统依赖（opencv、mediapipe需要）


# 复制代码
COPY  . /app

# 升级pip


# 安装Python依赖
RUN pip install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple

# 启动命令
CMD ["python", "peopleCheck.py"]
