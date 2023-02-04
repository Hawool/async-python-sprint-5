FROM python:3.11-bullseye

# install python libraries
COPY ./requirements.txt requirements.txt
RUN apt -y update \
    && pip install --upgrade pip \
    && pip install -r requirements.txt

COPY . code
WORKDIR code