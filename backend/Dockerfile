FROM python:3.7-slim-buster
WORKDIR /usr/app
COPY requirements.txt .
RUN apt-get -y update && \
    apt-get -y install nginx gcc git && \
    pip install -r requirements.txt
COPY . .
COPY nginx.conf /etc/nginx/nginx.conf
EXPOSE 8000
CMD ["./start.sh"]