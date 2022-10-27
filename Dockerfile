# To enable ssh & remote debugging on app service change the base image to the one below
# FROM mcr.microsoft.com/azure-functions/python:4-python3.9-appservice
FROM mcr.microsoft.com/azure-functions/python:4-python3.9

ENV AzureWebJobsScriptRoot=/home/site/wwwroot \
    AzureFunctionsJobHost__Logging__Console__IsEnabled=true
ENV GECKODRIVER_VER v0.31.0
ENV FIREFOX_VER 91.0
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN set -x \
   && apt update \
   && apt upgrade -y

RUN apt-get install -y --no-install-recommends apt-utils
RUN apt-get install -y wget \
        build-essential \
        libgl1-mesa-glx \
        libgtk-3-dev 
RUN wget --no-verbose -O /tmp/firefox.tar.bz2 https://download-installer.cdn.mozilla.net/pub/firefox/releases/${FIREFOX_VER}/linux-x86_64/en-US/firefox-${FIREFOX_VER}.tar.bz2 \
   && rm -rf /opt/firefox \
   && tar -C /opt -xjf /tmp/firefox.tar.bz2 \
   && rm /tmp/firefox.tar.bz2 \
   && mv /opt/firefox /opt/firefox-${FIREFOX_VER} \
   && ln -fs /opt/firefox-${FIREFOX_VER}/firefox /usr/bin/firefox

  
RUN apt install -y wget bzip2 libxtst6 \
   packagekit-gtk3-module libx11-xcb-dev \
   libdbus-glib-1-2 libxt6 libpci-dev && \
   rm -rf /var/lib/apt/lists/*
# Add geckodriver
RUN set -x \
   && curl -sSLO https://github.com/mozilla/geckodriver/releases/download/${GECKODRIVER_VER}/geckodriver-${GECKODRIVER_VER}-linux64.tar.gz \
   && tar zxf geckodriver-*.tar.gz \
   && mv geckodriver /usr/bin/

COPY requirements.txt /
RUN pip install -r /requirements.txt

COPY . /home/site/wwwroot