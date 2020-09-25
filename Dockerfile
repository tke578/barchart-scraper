FROM python:3.8-slim

### debian mirror
RUN echo "deb http://cdn-aws.deb.debian.org/debian  stable main\ndeb http://cdn-aws.deb.debian.org/debian-security  stable/updates main" > /etc/apt/sources.list

# install dependencies
RUN apt-get update \
&& apt-get install -y wget gnupg apt-utils python3-pip git vim curl \
&& wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
&& sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list' \
&& apt-get update \
&& apt-get install -y google-chrome-stable fonts-ipafont-gothic fonts-wqy-zenhei fonts-thai-tlwg fonts-kacst fonts-freefont-ttf libxss1 \
--no-install-recommends \
&& apt-get install \
&& rm -rf /var/lib/apt/lists/*


ENV TZ=America/Los_Angeles
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone


WORKDIR /app

COPY . /app




RUN pip install --upgrade pip
RUN pip3 install -r requirements.txt



CMD [ "python3", "main_func.py"]