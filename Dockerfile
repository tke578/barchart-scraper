FROM python:3.8-slim

### debian mirror
RUN echo "deb http://cdn-aws.deb.debian.org/debian  stable main\ndeb http://cdn-aws.deb.debian.org/debian-security  stable/updates main" > /etc/apt/sources.list

# install dependencies
RUN apt-get update && apt-get install -y \
apt-utils \
python3-pip \
nginx \
supervisor \
git \
vim \
curl \
wget \ 
software-properties-common \
&& rm -rf /var/lib/apt/lists/*


#intall firefox
RUN apt-key adv --keyserver keyserver.ubuntu.com --recv-keys A6DCF7707EBC211F
RUN apt-add-repository "deb http://ppa.launchpad.net/ubuntu-mozilla-security/ppa/ubuntu bionic main"
RUN apt update
RUN apt install -y firefox

#install webdriver
RUN wget https://github.com/mozilla/geckodriver/releases/download/v0.27.0/geckodriver-v0.27.0-linux64.tar.gz \
	&& tar -xvzf geckodriver* \
	&& chmod +x geckodriver \
	&& mv geckodriver /usr/local/bin


ENV TZ=America/Los_Angeles
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone



COPY /app /app
COPY /config /config


RUN pip install --upgrade pip
RUN pip3 install -r /config/requirements.txt


# setup config
COPY config/nginx.conf /etc/nginx/sites-enabled/
COPY /config/app.ini /config/
COPY /config/supervisor.conf /etc/supervisor/conf.d/

RUN echo "\ndaemon off;" >> /etc/nginx/nginx.conf
RUN rm /etc/nginx/sites-enabled/default


EXPOSE 8080

CMD ["supervisord", "-n"]