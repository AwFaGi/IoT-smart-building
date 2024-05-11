FROM python:latest

WORKDIR /device/

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .