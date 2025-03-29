FROM python:3.11

RUN apt-get update && apt-get install -y python3-tk iproute2 x11-apps python3-pip openssl && pip3 install aioquic

ENV DISPLAY=host.docker.internal:0.0

WORKDIR /app
COPY . .
CMD ["python", "client_QUIC.py"]
