FROM python:3.11

RUN apt-get update && apt-get install -y python3-tk x11-apps

ENV DISPLAY=host.docker.internal:0.0

WORKDIR /app
COPY . .
CMD ["python", "server_TCP.py"]
