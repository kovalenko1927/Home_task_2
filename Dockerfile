
FROM ubuntu:latest

RUN apt-get update -y
RUN apt-get install -y python3-pip python-dev build-essential

COPY . /home

WORKDIR /home

RUN pip install -r requirements.txt


CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]
