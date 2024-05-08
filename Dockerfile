FROM python:3.12-slim

WORKDIR /pantip_trend_cronjob

ADD . /pantip_trend_cronjob

RUN apt-get update
RUN apt-get install -y wget cron

RUN wget -q https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
RUN apt-get install -y ./google-chrome-stable_current_amd64.deb

COPY crontab /etc/cron.d/crontab
RUN crontab /etc/cron.d/crontab

RUN pip install pipenv
RUN pipenv install --ignore-pipfile --system

CMD ["cron", "-f"]