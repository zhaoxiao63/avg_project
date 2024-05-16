# 使用官方的 OpenJDK 8 作为基础镜像
FROM openjdk:8-jdk

# 更新软件包列表并安装 Python 3.10 和其他必要的依赖项
RUN apt-get update && \
    apt-get install -y python3.9 pip && \
    apt-get clean

# 将 Python 3.10 设置为默认的 Python 版本
RUN update-alternatives --install /usr/bin/python python /usr/bin/python3.9 1

# 复制 requirements.txt 并安装 Python 依赖项
ADD /requirements.txt /
RUN pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r /requirements.txt

# 复制项目目录
ADD /src /src/
ADD /common /src/common
ADD /config /src/config
ADD /data_gen /src/data_gen
ADD /src/dependencies /src/dependencies

# 设置时区为亚洲/上海
ENV TZ=Asia/Shanghai
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# 设置工作目录
WORKDIR /src

# 启动命令
#CMD ["python", "/src/main.py"]
