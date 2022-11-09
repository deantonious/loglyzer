FROM python:3.11.0-alpine
LABEL maintainer="@deantonious"

RUN mkdir /app
WORKDIR /app
COPY . /app
RUN apk update && apk upgrade --available && python3 -m pip install --upgrade pip
RUN pip install -r /app/requirements.txt

ENTRYPOINT ["python3", "-m", "loglyzer"]
