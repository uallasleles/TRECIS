FROM openalpr/agent:4.1.1-arm64 as final-stage
# FROM openalpr/agent:latest as final-stage

WORKDIR /home

COPY [".", "/home"]

RUN apt-get update
RUN apt-get install -y software-properties-common 
RUN add-apt-repository ppa:deadsnakes/ppa 
RUN apt-get install -y curl
RUN apt-get install -y python3.9 \
  && cd /usr/local/bin \
  && ln -sf /usr/bin/python3 python
  # && ln -sf /usr/bin/python3.9 python3
  # && update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.6 1 \
  # && update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.9 2 \
  # && update-alternatives --set python /usr/bin/python3.9

RUN apt-get install -y python3-pip python3-dev python3-numpy python3-opencv \
  && pip3 install --no-cache-dir --upgrade pip \
  && pip3 install --no-cache-dir greenstalk==2.0.0 \
  && pip3 install --no-cache-dir aiostalk==1.0 \
  && pip3 install --no-cache-dir opencv-python \
  && pip3 install --no-cache-dir openalpr \
  # && apt-get install openalpr-daemon
  && rm -rf /var/lib/apt/lists/*

# CMD ["python", "recognizer.py"]