FROM python:3.8-slim-buster


RUN apt update
RUN apt -y install wget gnupg2 lsb-release

RUN echo "deb https://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list
RUN wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | apt-key add -

RUN apt -y update
RUN apt -y install postgresql-client-15

# copy files
COPY ./main.py /home/
COPY ./env-local.sh /home/envs/
COPY ./run.sh /home/

# pick working directory
WORKDIR /home/

# make scripts executable
RUN chmod +x run.sh
RUN chmod +x envs/env-local.sh

ENTRYPOINT ["./run.sh" ]
