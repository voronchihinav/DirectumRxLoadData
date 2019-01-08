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
CMD ["main.py", "-e", "psql", "-ht", "192.168.48.33", "-d", "LoadRX", "-n", "postgres", "-p", "11111", "-pr", "5436"]