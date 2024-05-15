# coding: utf-8

FROM python:3.10

ADD /requirements.txt /
RUN  pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r /requirements.txt

ADD /src /src/
ADD /common /src/common
ADD /config /src/config
ADD /data_gen /src/data_gen
ADD /dependencies /src/dependencies

ENV TZ=Asia/Shanghai
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

WORKDIR /src


CMD ["python",  "/src/main.py"]
