FROM python:2.7-alpine

RUN apk add --no-cache curl pkgconfig

ADD ./requirements.txt /opt/webapp-conntest/

WORKDIR /opt/webapp-conntest

RUN pip install -r requirements.txt

ADD . /opt/webapp-conntest

EXPOSE 8080

ENTRYPOINT ["python", "app.py"]