FROM ubuntu:latest
MAINTAINER Aleksandr Voronchihin 'voronchihinav@gmail.com'
RUN apt-get update -y
RUN apt-get install
RUN apt-get install -y python3-pip python3-dev build-essential
RUN apt-get install -y locales
RUN locale-gen en_US.UTF-8
COPY . /app
WORKDIR /app
RUN pip3 install -r requirements.txt
EXPOSE 5555
ENV LANG='en_US.UTF-8' LC_ALL='en_US.UTF-8'