FROM ubuntu:latest

# Update and install necessary packages
RUN apt-get update -y && \
    apt-get install -y python3-pip python3-dev build-essential python3-venv libpq-dev python3-full locales && \
    locale-gen en_US.UTF-8

# Set environment variables
ENV LANG='en_US.UTF-8' LC_ALL='en_US.UTF-8'

# Copy the application code to the container
COPY . /app

# Create the virtual environment
RUN python3 -m venv myenv

# Activate the virtual environment and install dependencies
RUN /bin/bash -c "source myenv/bin/activate && pip install -r /app/requirements.txt"

WORKDIR /app

# Expose the port
EXPOSE 5555
