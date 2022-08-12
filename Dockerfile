FROM python:slim-bullseye
RUN  apt-get update \
    && apt-get upgrade -y
COPY . /usr/src/app
WORKDIR /usr/src/app
RUN pip3 install --no-cache-dir -r requirements.txt
ENTRYPOINT [ "python", "./kicktippbb.py" ]
