FROM ubuntu:latest
MAINTAINER Aleksandr Voronchihin 'voronchihinav@gmail.com'
RUN apt-get update -y
RUN apt-get install -y python-pip python-dev build-essential
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
ENV ENGINE psql
EXPOSE 5555
ENTRYPOINT ["python"]
CMD ["main.py", "-e", "${ENGINE}", "-ht", "${HOST}", "-d", "${DB}", "-n", "${USER}", "-p", "${PWD}", "-pr", "${PORT}"]