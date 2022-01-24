FROM ubuntu:18.04

# 1. 기본 파일 설치
## 1-1. before update clean
RUN apt-get clean
## 1-1. Upgrade installed packages
RUN apt-get update && apt-get upgrade -y && apt-get clean
## 1-2. Upgrade installed libraries
RUN apt-get install -y curl vim wget build-essential

# 2. 파이썬 설치
## 2-1. Python package management and basic dependencies
RUN apt-get install -y curl python3.7 python3.7-dev python3.7-distutils
## 2-2. Register the version in alternatives
RUN update-alternatives --install /usr/bin/python python /usr/bin/python3.7 1
## 2-3. Set python 3 as the default python
RUN update-alternatives --set python /usr/bin/python3.7
## 2-4. Upgrade pip to latest version
RUN curl -s https://bootstrap.pypa.io/get-pip.py -o get-pip.py && python get-pip.py --force-reinstall && rm get-pip.py

# 3. 패키시 추가 및 경로 변경
## 3-1. install other package
WORKDIR /user/local
RUN pip install --upgrade pip
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

WORKDIR /user/local
RUN mkdir flask_chat_server
WORKDIR ./flask_chat_server
COPY . .

## 3-2. 환경설정
RUN apt-get install -y locales
RUN locale-gen ko_KR.UTF-8
ENV LANG en_US.UTF-8
ENV PYTHONIOENCODING=UTF-8
RUN ln -sf /usr/share/zoneinfo/Asia/Seoul /etc/localtime
ENV PYTHONUNBUFFERED=1

ENV FLASK_APP chat_server_start.py
ENV FLASK_RUN_HOST 0.0.0.0

CMD gunicorn chat_server_start:app --worker-class eventlet -w 1 -b 0.0.0.0:9094  --reload