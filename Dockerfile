FROM python:3.10.4

WORKDIR /src
ENV PYTHONPATH "${PYTHONPATH}:/src"
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip

COPY ./requirements.txt /src


RUN pip install -r requirements.txt

COPY . /src