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

# 3. 메캅 설치
# mecab설치 - 참조 : https://bitbucket.org/eunjeon/mecab-ko-dic/src/master/
WORKDIR /usr/local/lib
RUN wget "https://bitbucket.org/eunjeon/mecab-ko/downloads/mecab-0.996-ko-0.9.2.tar.gz"
RUN tar zxfv mecab-0.996-ko-0.9.2.tar.gz
WORKDIR ./mecab-0.996-ko-0.9.2
RUN ./configure
RUN make
RUN make install

WORKDIR /usr/local/lib
RUN wget "https://bitbucket.org/eunjeon/mecab-ko-dic/downloads/mecab-ko-dic-2.0.1-20150920.tar.gz"
RUN tar zxfv mecab-ko-dic-2.0.1-20150920.tar.gz
RUN apt-get install -y automake1.11
WORKDIR ./mecab-ko-dic-2.0.1-20150920
RUN ./autogen.sh
RUN ./configure
RUN make
RUN make install

# user-dictionary add
WORKDIR /usr/local/lib
WORKDIR ./mecab-ko-dic-2.0.1-20150920
RUN ./tools/add-userdic.sh
RUN make clean
RUN make install

# Mecab Python install
WORKDIR /user/local
RUN cp /usr/local/lib/mecab-0.996-ko-0.9.2/mecab-config /usr/bin
RUN pip install python-mecab-ko

# 4. 패키시 추가 및 경로 변경
## 4-1. install other package
WORKDIR /user/local
RUN pip install --upgrade pip
#COPY requirements.txt requirements.txt
#RUN pip3 install -r requirements.txt


WORKDIR /user/local
COPY ./mecab_service/mecab_ner_app/requirements.txt /user/local/
RUN pip install -r requirements.txt
COPY ./mecab_service/mecab_ner_app /user/local/
COPY ./chat_core /user/local/app/chat_core


## 4-2. 환경설정
RUN apt-get install -y locales
RUN locale-gen ko_KR.UTF-8
ENV LANG en_US.UTF-8
ENV PYTHONIOENCODING=UTF-8
RUN ln -sf /usr/share/zoneinfo/Asia/Seoul /etc/localtime

#CMD ["uvicorn", "app.infrastructure.fastapi.main:app", "--host", "0.0.0.0", "--port", "5100"]
