FROM python:3.11-bullseye

RUN apt update

# install python libraries
COPY ./requirements.txt requirements.txt
RUN pip install --upgrade pip

RUN pip install -r requirements.txt

COPY . code
WORKDIR code