FROM python:3.10

RUN apt-get update

RUN mkdir /opt/scratch

COPY "./test.py" /opt/scratch

WORKDIR /opt/scratch

CMD ["python3","test.py"]
