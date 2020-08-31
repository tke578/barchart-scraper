FROM python:3.8-slim

### debian mirror
RUN echo "deb http://cdn-aws.deb.debian.org/debian  stable main\ndeb http://cdn-aws.deb.debian.org/debian-security  stable/updates main" > /etc/apt/sources.list

# install dependencies
RUN apt-get update && apt-get install -y \
apt-utils \
python3-pip \
git \
vim \
curl \
&& rm -rf /var/lib/apt/lists/*


ENV TZ=America/Los_Angeles
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone


WORKDIR /app

COPY ./requirements.txt /app

COPY ./main_func.py /app

COPY ./heroku.yml /app


RUN pip install --upgrade pip
RUN pip3 install -r requirements.txt



CMD [ "python3", "main_func.py"]