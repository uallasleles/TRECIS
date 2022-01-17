FROM python:3.6.8-alpine3.9

ENV GROUP_ID=1000 \
    USER_ID=1000

WORKDIR /var/www

COPY requirements.txt /var/www/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /var/www/

RUN pip install --no-cache-dir gunicorn==20.1.0

RUN addgroup --gid $GROUP_ID www && \
    adduser -D --uid $USER_ID -G www www --shell /bin/sh

USER www

EXPOSE 5000

CMD ["gunicorn", "-w", "4", "--bind", "0.0.0.0:5000", "wsgi"]