FROM python:3.9.7-alpine3.14
RUN pip install flask
WORKDIR /app
ENV APP_STARTUP_DELAY 0
COPY app.py .
ENTRYPOINT ["python", "app.py"]