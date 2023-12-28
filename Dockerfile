FROM python:3.8-slim-buster


# -------------------install pg dump dependencies
RUN apt update
RUN apt -y install wget gnupg2 lsb-release

RUN echo "deb https://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list
RUN wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | apt-key add -

RUN apt -y update
RUN apt -y install postgresql-client-15

RUN apt-get -y install postgresql-15
# -------------------install pg dump dependencies

# copy files
COPY ./main.py /home/
COPY ./requirements.txt /home/
COPY ./run.sh /home/

# env-local.sh is a placeholder file that is replaced
# when running image in cloud
RUN mkdir /envs/
RUN touch /envs/env-local.sh

# make directory for dumped db files
RUN mkdir /home/dumped_files

# pick working directory
WORKDIR /home

# make scripts executable
RUN chmod +x run.sh
RUN pip install -r requirements.txt

ENTRYPOINT ["./run.sh" ]
