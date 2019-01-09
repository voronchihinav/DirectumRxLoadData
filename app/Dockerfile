FROM ubuntu:latest
MAINTAINER Aleksandr Voronchihin 'voronchihinav@gmail.com'
RUN apt-get update -y
RUN apt-get install
RUN apt-get install -y python3-pip python3-dev build-essential
COPY . /app
WORKDIR /app
RUN pip3 install -r requirements.txt
ENV ENGINE psql
EXPOSE 5555
ENTRYPOINT ["python3"]
CMD ["main.py", "-e", "psql", "-ht", "192.168.48.33", "-d", "LoadRX", "-n", "postgres", "-p", "11111", "-pr", "5436"]