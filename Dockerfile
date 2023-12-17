FROM python:3.8-slim-buster


RUN apt update
RUN apt -y install wget gnupg2 lsb-release

RUN echo "deb https://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list
RUN wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | apt-key add -

RUN apt -y update
RUN apt -y install postgresql-client-15

COPY ./main.py /home/
WORKDIR /home/

ENTRYPOINT ["python", "main.py" ]
