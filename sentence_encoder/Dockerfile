FROM tensorflow/tensorflow:2.0.1-py3
WORKDIR /usr/app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["./start.sh"]