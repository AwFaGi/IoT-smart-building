FROM python:latest

WORKDIR /server/

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .