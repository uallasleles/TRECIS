FROM python:3.9.7-alpine

WORKDIR /home

COPY . /home

RUN apk add --update-cache && \
    apk --no-cache add beanstalkd && \ 
    python -m pip install --upgrade pip && \
    pip install --no-cache-dir greenstalk && \
    pip install --no-cache-dir aiostalk==1.0 && \
    pip install --no-cache-dir aiohttp==3.8.1 && \
    pip install --no-cache-dir pymongo==4.0.1 && \
    pip install --no-cache-dir requests==2.27.1 && \
    crontab crontab

# Setting up a working directory
ENV WORKDIR /usr/local/work
ENV AUTO_RUN_DIR /docker-entrypoint-initdb.d
ENV BEANSTALKD start_beanstalkd.sh
RUN mkdir -p $WORKDIR

# Initialization commands for replicating databases
COPY ./$BEANSTALKD $AUTO_RUN_DIR/

RUN chmod +x $AUTO_RUN_DIR/$BEANSTALKD

WORKDIR /home

RUN chmod +x alpr_consumer.py
RUN nohup -u ./alpr_consumer.py &

RUN chmod +x preprocessor.py
RUN nohup -u ./preprocessor.py &

RUN chmod +x manager.py
RUN nohup -u ./manager.py &

CMD ["crond", "-f"]