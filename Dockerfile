# syntax=docker/dockerfile:1

FROM python:3.10-slim-buster

RUN apt-get update

RUN apt-get install build-essential -y

RUN apt-get install -y libjpeg-dev libpng-dev libtiff-dev libgtk-3-dev libavcodec-extra libavformat-dev libswscale-dev libv4l-dev libxvidcore-dev libx264-dev libatlas-base-dev gfortran libeigen3-dev libtbb-dev

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip3 install --upgrade pip

RUN pip3 install -r requirements.txt


COPY . .

CMD [ "uvicorn", "main:app" , "--reload", "--host", "0.0.0.0"]