FROM python:3.6.8-alpine3.9
# FROM uallasleles/flask:latest

LABEL MAINTAINER="Uallas Leles Pereira <uallasleles@hotmail.com>"

ENV GROUP_ID=1000 \
    USER_ID=1000

WORKDIR /var/www/

ADD ./requirements.txt /var/www/requirements.txt
RUN pip install -r requirements.txt --no-cache-dir

ADD . /var/www/
RUN pip install gunicorn

RUN addgroup -g $GROUP_ID www
RUN adduser -D -u $USER_ID -G www www -s /bin/sh

USER www

EXPOSE 5000

CMD ["gunicorn", "-w", "4", "--bind", "0.0.0.0:5000", "wsgi"]