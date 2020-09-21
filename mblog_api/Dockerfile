FROM python:3.6-slim

WORKDIR /app/mblog
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8080
ENTRYPOINT [ "python", "./mblog_api.py" ]
