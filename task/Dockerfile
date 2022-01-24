FROM python:3.6.12-alpine3.12

COPY . .

RUN apk update && apk add bash

RUN pip install -r requirements.txt

COPY wait-for-it.sh /wait-for-it.sh

RUN chmod +x /wait-for-it.sh

RUN crontab crontab

CMD ["crond", "-f"]