# To enable ssh & remote debugging on app service change the base image to the one below
# FROM mcr.microsoft.com/azure-functions/python:4-python3.9-appservice
FROM mcr.microsoft.com/azure-functions/python:4-python3.9

ENV AzureWebJobsScriptRoot=/home/site/wwwroot \
    AzureFunctionsJobHost__Logging__Console__IsEnabled=true
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

  
RUN apt install -y wget bzip2 libxtst6 \
   packagekit-gtk3-module libx11-xcb-dev \
   libdbus-glib-1-2 libxt6 libpci-dev && \
   rm -rf /var/lib/apt/lists/*

COPY requirements.txt /
RUN pip install -r /requirements.txt

COPY . /home/site/wwwroot