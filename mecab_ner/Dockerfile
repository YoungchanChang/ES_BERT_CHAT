FROM ubuntu:18.04

ENV DEBIAN_FRONTEND noninteractive

# 1. Install basic package
## 1-1. Upgrade installed packages
RUN apt-get update && apt-get upgrade -y && apt-get clean

## 1-2. 기본 파일 설치
RUN apt-get -y install curl vim wget build-essential

# 2. Install Python
## 2-1. Python package management and basic dependencies
RUN apt-get install -y software-properties-common
RUN add-apt-repository ppa:deadsnakes/ppa

## 2-2. Install py39 from deadsnakes repository
RUN apt-get install -y curl python3.9 python3.9-dev python3.9-distutils

## 2-3. Install pip from standard ubuntu packages
RUN apt-get install -y python3-pip python-pip

## 2-4. To solve 'HTMLParser' object has no attribute error
RUN pip3 install --upgrade setuptools
RUN pip3 install --upgrade pip
RUN pip3 install --upgrade distlib

## 2-5. Register the version in alternatives
RUN update-alternatives --install /usr/bin/python python /usr/bin/python3.9 1

## 2-3. Set python 3 as the default python
RUN update-alternatives --set python /usr/bin/python3.9


# 3. Install mecab
# 참조 : https://bitbucket.org/eunjeon/mecab-ko-dic/src/master/
## 3-1. mecab-ko 설치
WORKDIR /usr/local/lib
RUN wget "https://bitbucket.org/eunjeon/mecab-ko/downloads/mecab-0.996-ko-0.9.2.tar.gz"
RUN tar zxfv mecab-0.996-ko-0.9.2.tar.gz
WORKDIR ./mecab-0.996-ko-0.9.2
RUN ./configure
RUN make
RUN make install

## 3-2. mecab-ko-dic 설치
WORKDIR /usr/local/lib
RUN wget "https://bitbucket.org/eunjeon/mecab-ko-dic/downloads/mecab-ko-dic-2.0.1-20150920.tar.gz"
RUN tar zxfv mecab-ko-dic-2.0.1-20150920.tar.gz
RUN apt-get install -y automake1.11
WORKDIR ./mecab-ko-dic-2.0.1-20150920
RUN ./autogen.sh
RUN ./configure
RUN make
RUN make install

## 3-3. user-dictionary add
WORKDIR /usr/local/lib
WORKDIR ./mecab-ko-dic-2.0.1-20150920
RUN ./tools/add-userdic.sh
RUN make clean
RUN make install

## 3-4. python-mecab-ko for Mecab Python install
RUN cp /usr/local/lib/mecab-0.996-ko-0.9.2/mecab-config /usr/bin
RUN pip install python-mecab-ko
RUN pip install mecab-python3

#### environment setting
RUN apt-get install -y locales
RUN locale-gen ko_KR.UTF-8
ENV LANG en_US.UTF-8
ENV PYTHONIOENCODING=UTF-8
RUN ln -sf /usr/share/zoneinfo/Asia/Seoul /etc/localtime


# flask_environment
WORKDIR /user/local
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
RUN apt-get install -y gunicorn3
WORKDIR /user/local
RUN mkdir mecab_ner
WORKDIR ./mecab_ner
COPY . .

ENV FLASK_APP app_start.py
ENV FLASK_RUN_HOST 0.0.0.0

CMD gunicorn3 app_start:app -b 0.0.0.0:9090 -w 2 --threads 2 --timeout 600