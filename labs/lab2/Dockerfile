FROM python:3

WORKDIR /app
COPY . .
RUN pip install 'click'
RUN apt-get update
RUN apt-get install -y iputils-ping

ENTRYPOINT [ "python3", "mtu.py" ]
CMD [ "google.com" ]
