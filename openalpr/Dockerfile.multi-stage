FROM openalpr/agent:latest as final-stage

LABEL MAINTAINER="Uallas Leles Pereira <uallasleles@hotmail.com>"

ARG RTSP_SOURCE

WORKDIR /

COPY ["recognize.py", "/home"]

RUN apt-get update
RUN apt-get install -y wget \
  && apt-get install -y nano \
  && apt-get install -y python3-pip python3-dev \
  && cd /usr/local/bin \
  && ln -s /usr/bin/python3 python \
  && pip3 --no-cache-dir install --upgrade pip \
  && pip3 install opencv-python \
  && pip3 install openalpr \
  && pip3 install requests \
  && rm -rf /var/lib/apt/lists/*

