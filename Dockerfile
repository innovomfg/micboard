FROM python:3

MAINTAINER Karl Swanson <karlcswanson@gmail.com>

WORKDIR /usr/src/app

ENV TZ=America/New_York
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
RUN curl -fsSL https://deb.nodesource.com/setup_23.x -o nodesource_setup.sh | bash -
RUN apt-get clean && apt-get update
RUN apt-get install nodejs npm -y

COPY . .

RUN python3 -m pip install -r py/requirements.txt
RUN set npm_config_python=/usr/bin/python3
RUN npm install 
RUN npm run build

EXPOSE 8058

CMD ["python3", "py/micboard.py"]
