FROM openalpr/agent:latest as final-stage

WORKDIR /home

COPY [".", "/home"]

RUN apt-get update
RUN apt-get install -y python3-pip python3-dev \
  && pip3 install --no-cache-dir -r requirements.txt \
  && cd /usr/local/bin \
  && ln -s /usr/bin/python3 python \
  && pip3 install --no-cache-dir --upgrade pip \
  && pip3 install --no-cache-dir opencv-python \
  && pip3 install --no-cache-dir openalpr \
  && rm -rf /var/lib/apt/lists/*

CMD ["python", "recognize.py"]