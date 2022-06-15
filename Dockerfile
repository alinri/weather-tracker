FROM python:3.10.5-alpine3.16

ENV WEATHER_DB_HOST=''
ENV WEATHER_DB_USERNAME=''
ENV WEATHER_DB_PASSWORD=''
ENV WEATHER_DB_NAME=''
ENV WEATHER_API_KEY=''

RUN apk update && apk add --virtual build-deps gcc python3-dev musl-dev && apk add --no-cache mariadb-dev

RUN addgroup -S app && adduser -S app -G app

WORKDIR /myapp
ADD . .

RUN chmod 755 script.sh
RUN chmod 755 entry.sh
RUN apk add --update busybox-suid
USER app

RUN pip3 install ez_setup
RUN pip3 install -r requirements.txt

RUN /usr/bin/crontab /myapp/crontab.txt

USER root

RUN apk del build-deps

USER root

ENTRYPOINT ["/myapp/entry.sh"]
