FROM nvidia/cuda:10.1-cudnn7-devel

RUN apt-get update && apt-get install -y python3 python3-pip sudo

WORKDIR /opt

COPY . /opt/

RUN pip3 install -e .
RUN pip3 install -e .[torch]